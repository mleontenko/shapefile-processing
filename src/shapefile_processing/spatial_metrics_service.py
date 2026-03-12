import geopandas as gpd


class SpatialMetricsService:
    def calculate_area(self, gdf, column_name='area'):
        gdf[column_name] = gdf.geometry.area
        return gdf

    def calculate_perimeter(self, gdf, column_name='perimeter'):
        gdf[column_name] = gdf.geometry.length
        return gdf

    def calculate_distance_to_nearest_neighbor(self, gdf, column_name='dnn'):
        left = gdf.reset_index(drop=True)
        right = left.copy()

        try:
            nearest = gpd.sjoin_nearest(
                left,
                right,
                how='left',
                distance_col=column_name,
                lsuffix='left',
                rsuffix='right',
                max_distance=None,
                exclusive=True,
            )
        except TypeError:
            nearest = gpd.sjoin_nearest(
                left,
                right,
                how='left',
                distance_col=column_name,
                lsuffix='left',
                rsuffix='right',
                max_distance=None,
            )
            nearest = nearest[nearest.index != nearest['index_right']]

        dnn_by_index = nearest.groupby(nearest.index)[column_name].min()
        gdf[column_name] = gdf.reset_index(drop=True).index.to_series().map(dnn_by_index).values
        return gdf
