import rasterio
from rasterio.features import rasterize
import os
import geopandas as gpd


def create_footprint_channel():
    with rasterio.open('../../data/results/pan-arctic/Panarctic_iwp_area.tif') as src:
        profile = src.profile
        transform = src.transform
        crs = src.crs
        width = src.width
        height = src.height
        
    gdf = gpd.read_file('../../data/footprint/dissolve_footprints.geojson')
    if gdf.crs is None:
        raise ValueError("GeoDataFrame has no CRS defined.")
    if gdf.crs != crs:
        gdf = gdf.to_crs(crs)

    shapes = [(geom, 1) for geom in gdf.geometry if not geom.is_empty and geom.is_valid]

    mask = rasterize(shapes, out_shape=(height, width), transform=transform, fill=0, dtype='uint8')

    profile.update(dtype='uint8', count=1, compress='lzw', nodata=0)

    if os.exists('../../data/footprint/panarctic_footprint.tif'): 
        raise ValueError("File exists")
    else:
        with rasterio.open('../../data/footprint/panarctic_footprint.tif', 'w', **profile) as dst:
            dst.write(mask, 1)
    
    print("Footprint raster created successfully.")


def add_footprint_channel(output_dir):
    for root, _, files in os.walk('../../data/results/pan-arctic'):
        for file in files:
            if file.endswith('.tif') and not file.endswith('_footprint.tif'):
                stats_path = os.path.join(root, file)
                new_stats_path = stats_path.replace('.tif', '_footprint.tif')
                with rasterio.open(stats_path) as src1, rasterio.open(output_dir) as src2:
                    profile = src1.profile
                    profile.update(count=2)

                    with rasterio.open(new_stats_path, 'w', **profile) as dst:
                        dst.write(src1.read(1), 1)
                        dst.write(src2.read(1), 2)

def merge_all_stats(output_dir):
    input_rasters = []
    for root, _, files in os.walk('../../data/results/pan-arctic'):
        for file in files:
            if not file.endswith('_footprint.tif'):
                input_rasters.append(os.path.join(root, file))

    srcs = [rasterio.open(r) for r in input_rasters]

    profile = srcs[0].profile
    profile.update(count=len(input_rasters))

    with rasterio.open(output_dir, 'w', **profile) as dst:
        for i, src in enumerate(srcs):
            print(f"Updated profile for output raster: {profile}")
            print(f"Merging raster {input_rasters[i]} into output {output_dir} at band {i+1}")
            dst.write(src.read(1), i+1)



if __name__ == "__main__":
    # create_footprint_channel()
    
    #output_dir_footprint = '../../data/footprint/panarctic_footprint.tif'
    
    #add_footprint_channel(output_dir_footprint)

    output_raster = '../../data/results/pan-arctic/Pan-arctic_IWP_stats.tif'
    merge_all_stats(output_raster)