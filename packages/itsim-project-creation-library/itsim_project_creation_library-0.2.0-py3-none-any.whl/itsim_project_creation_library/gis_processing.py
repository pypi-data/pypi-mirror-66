from csv import DictReader
from geopandas import GeoDataFrame, read_file
from io import TextIOWrapper
from pyproj import Proj, transform
from shapely.geometry import Polygon
from zipfile import ZipFile
import pandas as pd
from pathlib import Path
from typing import (
    Any,
    Callable,
    List,
    Optional,
    Tuple,
    Union,
)
from collections import namedtuple
from os import devnull
from contextlib import redirect_stdout


def _dict_to_namedtuple(name, d):
    return namedtuple(name, d.keys())(**d)


# FIELDS FOR LAYERS PROPERTIES
dot_layer_props = _dict_to_namedtuple('DotLayerProps', {
    'TITLE': 'dot_title',
    'COLOR': 'dot_color',
    'RADIUS': 'dot_radius',
    'OPACITY': 'dot_opacity',
})

line_layer_props = _dict_to_namedtuple('LineLayerProps', {
    'TITLE': 'line_title',
    'COLOR': 'line_color',
    'WIDTH': 'line_width',
    'OPACITY': 'line_opacity',
    'ROUTE_TYPE': 'route_type',
})

shape_layer_props = _dict_to_namedtuple('ShapeLayerProps', {
    'TITLE': 'shape_title',
    'FILL_COLOR': 'shape_fill_color',
    'STROKE_COLOR': 'shape_stroke_color',
    'OPACITY': 'dot_opacity',
})

GALL_PETERS_CRS = '+proj=cea +lon_0=0 +lat_ts=45 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs'

WGS84_EPSG = 4326


# Format for PyDoc
# https://stackoverflow.com/a/24385103/1988874


def rough_intersection(
    data: GeoDataFrame,
    geometry: pd.Series,
) -> pd.DataFrame:
    """Intersecting data with a geometry.

    Args:
        data: the set of data to process
        geometry: the shape to follow to carry out the intersection

    Returns:
        data set that matches the given bbox
    """
    selector = data['geometry'].apply(lambda x: x.convex_hull.intersects(geometry))
    return data.loc[selector]


def calculate_density(
    data: GeoDataFrame,
    field_from: str,
    field_to: Optional[str] = None,
    area_field: Optional[str] = None,
    area_field_unit_in_km2: Optional[bool] = True,
) -> pd.DataFrame:
    """Calculate density for a zonal layer where data is expressed in absolute value.

    If the 'area_field' value is not given, the function will calculates it following the geometry of the given GeoDataFrame.
    If the 'field_to' value is not given, the function will create a new column with a name of the following format:
        "field_from_dens"

    Args:
        data: the input geodataframe
        field_from: name of the origin data column
        field_to: name of the caluclated density column that will be created by the function
        area_field: name of the column that contains the values of areas (must be expressed in km²)
        area_field_unit_in_km2: indicates if the area field unit is in km² (default) or m².

    Returns:
        input DataFrame with a new column that contains the density (in km²) calculated from 'field_from' column values.
    """
    result = data.to_crs(GALL_PETERS_CRS)
    if field_to is None:
        field_to = field_from + '_dens'
    if area_field:
        unit_adjustment = 1 if area_field_unit_in_km2 else 1e6
        result[field_to] = data[field_from] / data[area_field] / unit_adjustment
    else:
        # geopandas' area gives a value in m²
        result[field_to] = data[field_from] / data.area * 1e6
    return result


def convert_hectare_to_km2(data: pd.Series) -> pd.Series:
    """Convert areas expressed in hectare contained in the given data in km².

    Args:
        data: the series to process with values expressed in hectares

    Returns:
        processed series with values expressed in km²
    """
    return data / 100


def convert_km2_to_hectare(data: pd.Series) -> pd.Series:
    """Convert areas expressed in hectare contained in the given data in km².

    Args:
        data: the series to process with values expressed in km²

    Returns:
        processed series with values expressed in hectares
    """
    return data * 100


def get_stops_bbox_from_gtfs(
    gtfs_path: Union[str, Path],
    projection: Optional[str] = f'epsg:{WGS84_EPSG}',
) -> GeoDataFrame:
    """Return a bbox that contains the whole stops set included in the GTFS.

    Projects the bbox's dataframe in the given projection or in WGS84 by default.

    Args:
        gtfs_path: GTFS file path
        projection: projection in which the bbox should be expressed (WGS84 by default)

    Returns:
        bbox that contains the whole set of GTFS's stops
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
    bbox = get_bbox(min_lat=min_lat, max_lat=max_lat, min_lon=min_lon, max_lon=max_lon)
    bbox_projected = GeoDataFrame()
    bbox_projected['geometry'] = None
    bbox_projected.loc[0, 'geometry'] = Polygon(bbox)
    bbox_projected.crs = {'init': f'epsg:{WGS84_EPSG}'}
    if projection != WGS84_EPSG:
        return bbox_projected.to_crs({'init': projection})
    else:
        return bbox_projected


def calculate_area(
    data: GeoDataFrame,
    area_unit_in_km2: Optional[bool] = True,
) -> GeoDataFrame:
    """Calculate the area of the zones inclued in the given data expressed in the given projection.

    Then, this function converts the layer in the WGS84 projection.

    Args:
        data: set of data
        area_unit_in_km2 (optional, default true): unit to output the area should be in km² or m².

    Returns:
        given data with calculated areas in WGS84 projection ('calculated_area' column added)
    """
    reprojected_data = data.to_crs(GALL_PETERS_CRS)
    unit_factor = 1e6 if area_unit_in_km2 else 1
    reprojected_data['calculated_area'] = reprojected_data.area / unit_factor
    return reprojected_data


def _get_columns_to_keep(columns_to_keep, df_columns):
    return list(set(columns_to_keep) & set(df_columns))


def clean_layer(
    data: GeoDataFrame,
    *columns_to_keep: List[str],
) -> GeoDataFrame:
    """Return a cleaned version of the given data with only the given columns and the geometry.

    Args:
        data: content of a layer
        columns_to_keep: list of names of the colums to keep

    Returns:
        cleaned data
    """
    if 'geometry' not in columns_to_keep:
        columns_to_keep_with_geo = columns_to_keep + ('geometry',)
    columns_to_keep_with_geo = _get_columns_to_keep(columns_to_keep_with_geo, data.columns)
    return data.loc[:, columns_to_keep_with_geo]


def create_carroyage(
    carroyage_path: Union[str, Path],
    data_path: Union[str, Path],
    output_path: Union[str, Path],
    bbox: List[List[float]] = None,
    min_lat: float = None,
    max_lat: float = None,
    min_lon: float = None,
    max_lon: float = None
) -> None:
    """Process the carroyage, cuts it to the necessary bounding box and export the result into a shapefile.

    Args:
        carroyage_path: path to carroyage
        data_path: path to the population path
        output_path: path of the output path
        bbox: the bbox list
        min_lat: minimum latitude of bounding box
        max_lat: maximum latitude of bounding box
        min_lon: minimum longitude of bounding box
        max_lon: maximum longitude of bounding box
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


def read_population_data(path: Union[str, Path]) -> GeoDataFrame:
    """Read population data from carroyage.

    Args:
        path: the carroyage file path

    Returns:
        carroyage content, with id and ind_c columns
    """
    # for simpledbf to be silent on import
    with open(devnull, 'w') as f:
        with redirect_stdout(f):
            from simpledbf import Dbf5
    data = Dbf5(path)
    data_frame = data.to_dataframe()
    return data_frame.loc[:, ['id', 'ind_c']]  # only index and nb of popultation


def get_bbox(
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
) -> List[List[float]]:
    """Create a bbox list from coordinates.

    Args:
        min_lat: minimum latitude of bounding box
        max_lat: maximum latitude of bounding box
        min_lon: minimum longitude of bounding box
        max_lon: maximum longitude of bounding box

    Returns:
        bbox list
    """
    return [
        [min_lon, min_lat],
        [max_lon, min_lat],
        [max_lon, max_lat],
        [min_lon, max_lat],
        [min_lon, min_lat],
    ]


def get_coordinates_from_bbox(bbox: List[List[float]]) -> Tuple[float, float, float, float]:
    """Get coordinates from a given bbox.

    Args:
        bbox: a bonding box

    Returns:
        coordinates contained by the bbox in the following format:
            (min_lat, max_lat, min_lon, max_lon)
    """
    min_lat = bbox[0][1]
    max_lat = bbox[2][1]
    min_lon = bbox[0][0]
    max_lon = bbox[1][0]
    return (min_lat, max_lat, min_lon, max_lon)


def merge_layers(*data_frames: List[pd.DataFrame]) -> GeoDataFrame:
    """Regroup several layers of the same format in one dataframe

    Args:
        bbox: list of all datframes to merge

    Returns:
        the merged dataframe
    """
    return pd.concat(data_frames)


def merge_and_clean_layers(
    paths: List[str],
    *columns_to_keep: List[str],
) -> GeoDataFrame:
    """Create a layer from several shapefiles and clean it by only keeping columns of given names.

    The given shapefiles should be of the same format (same columns) as much as possible.
    It also projects the generated layer in WGS84.

    Args:
        paths: file paths to merge
        columns_to_keep: columns to keep during cleaning

    Returns:
        the generated dataframe
    """
    # Get first dataframe
    data = GeoDataFrame()
    for path in paths:
        data_to_add = read_file(path)
        data_to_add = clean_layer(data_to_add, *columns_to_keep)
        data = data.append(data_to_add)
    return data


def set_dots_properties(
    data: GeoDataFrame,
    title: Union[str, Callable[[pd.Series], Any]] = None,
    color: Union[str, Callable[[pd.Series], Any]] = None,
    radius: Union[str, float, Callable[[pd.Series], Any]] = None,
    opacity: Union[str, float, Callable[[pd.Series], Any]] = None,
) -> GeoDataFrame:
    """Set and standardize properties that will be used for the dots layer's display

    Args:
        data: the original data
        title: the field name containing the dot title or a callable that construct a dot title based on a column Series.
        color: the field name containing the dot color or a callable that construct a dot color based on a column Series.
        radius: the field name containing the dot radius or the value to set for every entry or a callable that construct
            a dot radius based on a column Series.
        opacity: the field name containing the dot opacity or the value to set for every entry or a callable that construct
            a dot radius based on a column Series.

    Returns:
        data with properties
    """
    result = data.copy()
    # title
    if callable(title):
        result.loc[:, dot_layer_props.TITLE] = result.apply(title, axis='columns')
    elif title != dot_layer_props.TITLE:
        result.rename(columns={title: dot_layer_props.TITLE}, inplace=True)
    # color
    if callable(color):
        result.loc[:, dot_layer_props.COLOR] = result.apply(color, axis='columns')
    elif color != dot_layer_props.COLOR:
        result.rename(columns={color: dot_layer_props.COLOR}, inplace=True)
    # radius
    if callable(radius):
        result.loc[:, dot_layer_props.RADIUS] = result.apply(radius, axis='columns')
    elif type(radius) is float:
        result.loc[:, dot_layer_props.RADIUS] = radius
    elif type(radius) is str:
        result.rename(columns={radius: dot_layer_props.RADIUS}, inplace=True)
    # opacity
    if callable(opacity):
        result.loc[:, dot_layer_props.OPACITY] = result.apply(opacity, axis='columns')
    if type(opacity) is float:
        result.loc[:, dot_layer_props.OPACITY] = opacity
    elif type(opacity) is str:
        result.rename(columns={opacity: dot_layer_props.OPACITY}, inplace=True)
    return result


def set_lines_properties(
    data: GeoDataFrame,
    title: Union[str, Callable[[pd.Series], Any]] = None,
    color: Union[str, Callable[[pd.Series], Any]] = None,
    width: Union[str, float, Callable[[pd.Series], Any]] = None,
    opacity: Union[str, float, Callable[[pd.Series], Any]] = None,
    route_type: Union[str, int, Callable[[pd.Series], Any]] = None,
) -> GeoDataFrame:
    """Set and standardize properties that will be used for the lines layer's display

    Args:
        data: the set of data to process
        title: the field name containing the line title or a callable that construct a line title based on a column Series.
        color: the field name containing the line color or a callable that construct a line color based on a column Series.
        route_type: the field name containing the route type or the value to set to every entry or a callable that construct
            a route type based on a column Series.
        width: the name of the field that contains the line width or the value to set to every entry (overrides width based on 'route_type' if given)
        opacity: the field name containing the line opacity or the value to set to every entry or a callable that construct a line opacity based on a
            column Series.

    Returns:
        data with properties
    """
    result = data.copy()
    # title
    if callable(title):
        result.loc[:, line_layer_props.TITLE] = result.apply(title, axis='columns')
    elif title != line_layer_props.TITLE:
        result.rename(columns={title: line_layer_props.TITLE}, inplace=True)
    # color
    if callable(color):
        result.loc[:, line_layer_props.COLOR] = result.apply(color, axis='columns')
    elif color != line_layer_props.COLOR:
        result.rename(columns={color: line_layer_props.COLOR}, inplace=True)
    # width
    if callable(width):
        result.loc[:, line_layer_props.WIDTH] = result.apply(width, axis='columns')
    if type(width) is float:
        result.loc[:, line_layer_props.WIDTH] = width
    elif type(width) is str:
        result.rename(columns={width: line_layer_props.WIDTH}, inplace=True)
    # opacity
    if callable(opacity):
        result.loc[:, line_layer_props.OPACITY] = result.apply(opacity, axis='columns')
    if type(opacity) is float:
        result.loc[:, line_layer_props.OPACITY] = opacity
    elif type(opacity) is str:
        result.rename(columns={opacity: line_layer_props.OPACITY}, inplace=True)
    # route_type
    if callable(route_type):
        result.loc[:, line_layer_props.ROUTE_TYPE] = result.apply(route_type, axis='columns')
    elif type(route_type) is int:
        result.loc[:, line_layer_props.ROUTE_TYPE] = route_type
    elif type(route_type) is str:
        result.rename(columns={route_type: line_layer_props.ROUTE_TYPE}, inplace=True)
    return result


def set_shapes_properties(
    data: GeoDataFrame,
    title: Union[str, Callable[[pd.Series], Any]] = None,
    fill_color: Union[str, Callable[[pd.Series], Any]] = None,
    stroke_color: Union[str, Callable[[pd.Series], Any]] = None,
    opacity: Union[str, float, Callable[[pd.Series], Any]] = None
) -> GeoDataFrame:
    """Set and standardize properties that will be used for the shapes layer's display

    Args:
        data: the set of data to process
        title: the field name containing the shape title or a callable that construct a shape title based on a column Series.
        fill_color: the field name containing the shape fill color or a callable that construct a shape fill color based on a column Series.
        stroke_color: the field name containing the shape stroke color or a callable that construct a shape stroke color based on a column Series.
        opacity: the field name containing the shape opacity or the value to set to every entry or a callable that construct a shape opacity based
            on a column Series.

    Returns:
        data with properties
    """
    result = data.copy()
    # title
    if callable(title):
        result.loc[:, shape_layer_props.TITLE] = result.apply(title, axis='columns')
    elif title:
        result.rename(columns={title: shape_layer_props.TITLE}, inplace=True)
    # fill color
    if callable(fill_color):
        result.loc[:, shape_layer_props.FILL_COLOR] = result.apply(fill_color, axis='columns')
    elif fill_color:
        result.rename(columns={fill_color: shape_layer_props.FILL_COLOR}, inplace=True)
    # stroke color
    if callable(stroke_color):
        result.loc[:, shape_layer_props.STROKE_COLOR] = result.apply(stroke_color, axis='columns')
    elif stroke_color:
        result.rename(columns={stroke_color: shape_layer_props.STROKE_COLOR}, inplace=True)
    # shape opacity
    if callable(opacity):
        result.loc[:, shape_layer_props.OPACITY] = result.apply(opacity, axis='columns')
    elif type(opacity) is float:
        result.loc[:, shape_layer_props.OPACITY] = opacity
    elif type(opacity) is str:
        result.rename(columns={opacity: shape_layer_props.OPACITY}, inplace=True)
    return result


def get_dot_properties_names() -> Tuple[str]:
    """Return a tuple continaing properties names for dot layer."""
    return tuple(dot_layer_props)


def get_line_properties_names() -> Tuple[str]:
    """Return a tuple continaing properties names for line layer."""
    return tuple(line_layer_props)


def get_shape_properties_names() -> Tuple[str]:
    """Return a tuple continaing properties names for shape layer."""
    return tuple(shape_layer_props)


def reproject_layer_in_WGS84(data: GeoDataFrame) -> GeoDataFrame:
    """
    Reproject the data frame to the WGS84 projection
    """
    return data.to_crs(epsg=WGS84_EPSG)
