from csv import DictReader
from geopandas import GeoDataFrame, read_file
from io import TextIOWrapper
from pyproj import Proj, transform
from shapely.geometry import Polygon
from simpledbf import Dbf5
from zipfile import ZipFile
import pandas as pd


# Format for PyDoc
# https://stackoverflow.com/a/24385103/1988874


def log_progress(message):
    print(message)


def rough_intersection(data, geometry):
    """Intersecting data with a geometry.

    Args:
        data (pandas.GeoDataFrame): the set of data to process
        geometry (pandas.Series): the shape to follow to carry out the intersection

    Returns:
        pandas.DataFrame: the data set that matches the given bbox
        
    """
    selector = data['geometry'].apply(lambda x: x.convex_hull.intersects(geometry))
    return data.loc[selector]


def compute_density(data, field_from, field_to, area_field):
    """Calculate density for a zonal layer where data is expressed in absolute value.

    If the 'area_field' value is not given, the function will calculates it following the geometry of the given GeoDataFrame.
    If the 'field_to' value is not given, the function will create a new column with a name of the following format:
        "field_from_dens"

    Args:
        data (geopandas.GeoDataFrame): the input geodataframe
        field_from (str): name of the origin data column
        field_to (str): name of the caluclated density column that will be created by the function
        area_field (str): name of the column that contains the values of areas (must be expressed in km²)

    Returns:
        pandas.DataFrame: the input DataFrame with a new column that contains the density calculated from 'field_from' column values.

    """
    if field_to is None:
        field_to = field_from + '_dens'
    if area_field:
        result.loc[:, field_to] = data.loc[:, field_from] / data.loc[:, area_field]
    else:
        # geopandas' area gives a value in m²
        result.loc[:, field_to] = data.loc[:, field_from] / (data.area / 10**6)
    return result


def hectare_to_km2(data):
    """Convert areas expressed in hectare contained in the given data in km².

    Args:
        data (pandas.Series): the series to process with values expressed in hectares

    Returns:
        pandas.Series: the processed series with values expressed in km²

    """
    result = data / 100
    return result


def km2_to_hectare(data):
    """Convert areas expressed in hectare contained in the given data in km².

    Args:
        data (pandas.Series): the series to process with values expressed in km²

    Returns:
        pandas.Series: the processed series with values expressed in hectares

    """
    result = data * 100
    return result


def get_stops_bbox_from_gtfs(gtfs_path, projection={'init': 'epsg:4326'}):
    """Return a bbox that contains the whole stops set included in the GTFS.

    Projects the bbox's dataframe in the given projection or in WGS84 by default.

    Args:
        gtfs_path (str): GTFS file path
        projection (Dict[str: str]): projection in which the bbox should be expressed (WGS84 by default)

    Returns:
        geopandas.GeoDataFrame: the bbox that contains the whole set of GTFS's stops

    """
    with ZipFile(gtfs_path) as archive:
        with archive.open("stops.txt") as f:
            with TextIOWrapper(f, encoding='utf-8-sig') as tf:
                reader = DictReader(tf)
                max_lat = -180
                min_lat = 180
                max_lon = -180
                min_lon = 180
                for line in reader:
                    max_lat = max(max_lat, float(line["stop_lat"]))
                    min_lat = min(min_lat, float(line["stop_lat"]))
                    max_lon = max(max_lon, float(line["stop_lon"]))
                    min_lon = min(min_lon, float(line["stop_lon"]))
    bbox = create_bbox(min_lat=min_lat, max_lat=max_lat, min_lon=min_lon, max_lon=max_lon)
    bbox_projected = GeoDataFrame()
    bbox_projected['geometry'] = None
    bbox_projected.loc[0, 'geometry'] = Polygon(bbox)
    bbox_projected.crs = {'init': 'epsg:4326'}
    bbox_projected = bbox_projected.to_crs(projection)
    return bbox_projected


def calculate_area_and_reproject_WGS84(data, epsg):
    """Calculate the area of the zones inclued in the given data expressed in the given projection.

    Then, this function converts the layer in the WGS84 projection.

    Args:
        data (geopandas.GeoDataFrame): set of data
        epsg (int): ID of the projection in which the layer is expressed

    Returns:
        geopandas.GeoDataFrame: given data with calculated areas in WGS84 projection ('calculated_area' column added)

    """
    reprojected_data = data.to_crs(epsg=epsg)
    reprojected_data['calculated_area'] = reprojected_data.area
    wgs84_data = data.to_crs(epsg=4326)
    return wgs84_data


def clean_layer_and_reproject_WGS84(data, columns_to_keep=[]):
    """Return a cleaned version of the given data converted in WGS84 projection (EPSG: 4326).

    Only the given columns and the layer geometry are kept.

    Args:
        data (geopandas.GeoDataFrame): content of a layer
        columns_to_keep (List[str]): list of names of the colums to keep

    Returns:
        geopandas.GeoDataFrame: the cleaned data

    """
    if 'geometry' not in columns_to_keep:
        columns_to_keep.append('geometry')
    cleaned_data = data.loc[:, columns_to_keep]
    wgs84_data = cleaned_data.to_crs(epsg=4326)
    return wgs84_data


def create_carroyage(carroyage_path, data_path, output_path, bbox=None, min_lat=None, max_lat=None, min_lon=None, max_lon=None):
    """Process the carroyage, cuts it to the necessary bounding box and export the result into a shapefile.

    Args:
        carroyage_path (str): path to carroyage
        data_path (str): path to the population path
        output_path (str): path of the output path
        bbox (List[List[float]]): the bbox list
        min_lat (float): minimum latitude of bounding box
        max_lat (float): maximum latitude of bounding box
        min_lon (float): minimum longitude of bounding box
        max_lon (float): maximum longitude of bounding box
    
    """
    carroyage = read_file(carroyage_path)
    population_data = read_population_data(data_path)
    carroyage = carroyage.merge(population_data, on='id')
    # selecting the carroyage in bbox_wgs84
    if min_lat or max_lat or min_lon or max_lon:
        proj_carroyage = Proj(carroyage.crs)
        proj_bbox = Proj(init='epsg:4326')
        # setting defaults
        if bbox is None:
            min_lat = min_lat or -90
            max_lat = max_lat or 90
            min_lon = min_lon or -180
            max_lon = max_lon or 180
        else:
            (min_lat, max_lat, min_lon, max_lon) = get_coordinates_from_bbox(bbox)
        # reprojecting
        max_lon, max_lat = transform(proj_bbox, proj_carroyage, max_lon, max_lat)
        min_lon, min_lat = transform(proj_bbox, proj_carroyage, min_lon, min_lat)
        carroyage = carroyage.cx[min_lon:max_lon, min_lat:max_lat]
    carroyage['pop_dens'] = carroyage['ind_c'] / (200 * 200 / 1e6)  # by definition, tiles are 200m wide
    carroyage = carroyage.to_crs(epsg=4326)
    carroyage.to_file(output_path)


def read_population_data(path):
    """Read population data from carroyage.

    Args:
        path (str): the carroyage file path

    Returns:
        geopandas.GeoDataFrame: the carroyage content

    """
    data = Dbf5(path)
    data_frame = data.to_dataframe()
    pop_data = data_frame.loc[:, ['id', 'ind_c']]  # only index and nb of popultation
    return pop_data


def create_bbox(min_lat, max_lat, min_lon, max_lon):
    """Create a bbox list from coordinates.

    Args:
        min_lat (float): minimum latitude of bounding box
        max_lat (float): maximum latitude of bounding box
        min_lon (float): minimum longitude of bounding box
        max_lon (float): maximum longitude of bounding box

    Returns:
        (List[List[float]]): the bbox list

    """
    return [
        [min_lon, min_lat],
        [max_lon, min_lat],
        [max_lon, max_lat],
        [min_lon, max_lat],
        [min_lon, min_lat],
    ]


def get_coordinates_from_bbox(bbox):
    """Get coordinates from a given bbox.

    Args:
        bbox (List[List[float]]): a bonding box

    Returns:
        (Tuple[float, float, float, float]): the coordinates contained by the bbox in the following format:
                                             (min_lat, max_lat, min_lon, max_lon)

    """
    min_lat = bbox[0][1]
    max_lat = bbox[2][1]
    min_lon = bbox[0][0]
    max_lon = bbox[1][0]
    return (min_lat, max_lat, min_lon, max_lon)

# Is this function still useful?
def merge_layers(data_frames):
    """Regroup several layers of the same format in one dataframe

    Args:
        bbox (List[pandas.DataFrame]): list of all datframes to merge

    Returns:
        geopandas.GeoDataFrame: the merged dataframe

    """
    result = pd.concat(data_frames)
    return result


def merge_and_clean_layers(paths, columns_to_keep):
    """Create a layer from several shapefiles and clean it by only keeping columns of given names.
    
    The given shapefiles should be of the same format (same columns) as much as possible.
    It also projects the generated layer in WGS84.

    Args:
        paths (List[str]): file paths to merge
        columns_to_keep (List[str]): columns to keep during cleaning

    Returns:
        geopandas.GeoDataFrame: the generated dataframe

    """
    # Get first dataframe
    data = GeoDataFrame()
    for path in paths:
        data_to_add = read_file(path)
        data_to_add = clean_layer_and_reproject_WGS84(data=data_to_add, columns_to_keep=columns_to_keep)
        data = data.append(data_to_add)
    return data
