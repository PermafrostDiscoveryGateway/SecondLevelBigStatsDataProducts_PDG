# Second-level big statistics data products for Ice Wedge Polygon (IWP) across Pan-Arctic
Generate a second-level statistics data products based on the IWP dataset from PDG


-------------------------------
## Repo walk-in tips
1. Tutorials: this foloder contains all the detailed progresses we have done to produce this big data product along the project. It consists of three python files that introduce every step to generate results.

   *gpkg_statstistics_mapping_noDatabase_alaska*: the code using geopackages to generate big stats maps. (This is what we use currently.)

   *shapefile_CountMap*: the code using shapefile to generate only count maps.

   *shapefile_CoverageMap*: the code using shapefile to generate coverage heat maps.
   
3. Data: this folder contains the part of the results we have generated in Alaska region.
   This folder contains part of final stats: IWP count, IWP area, length (diameter) sum/max/min/median/mean/perimeter, width, LCP count.
  
4. src: this foloder contains two sub project: 1) using geopackages. 2) using shapefile.

-------------------------------





## 1. Objectives
Ice Wedge (IW) is a crack in the ground formed by a narrow or thin piece of ice that measures up to 3–4 meters in length at ground level. As IW gets deeper, Ice Wedge Polygons are formed. The large number of IWPs across the entire Pan-Arctic region were extracted and organized by PDG (either in geopackage or shapefile format in an arctic projection EPSG:3413).

The goal of this project is to analysis the polygons, and generate data products to describe different profiles of IWP. This include: 

* IWP count maps.
* Area sum
* Length(diameter) sum/min/max/median/mean/std
* Perimeter sum
* Width sum
* LCP count

(We also generate some other side products, such as heatmap maps.)

This tutorial will walk you through how to download these Ice Wedge Polygon (IWP), how to process the data in batch, and finally generate big statistics data products. 

## 2. Overall big data production workflow

![image](https://github.com/user-attachments/assets/fb7c5960-4a8f-4f73-8198-dcf7df5d818c)
1) Our previous work have 


## 3. Project datasets
### 1) IWP polygon dataset
Introduction
https://arcticdata.io/catalog/view/doi:10.18739/A2KW57K57

Dataset API

(geopackages)
https://arcticdata.io/data/10.18739/A2KW57K57/iwp_geopackage_high/WGS1984Quad/

(shapefile)
https://arcticdata.io/data/10.18739/A2KW57K57/iwp_shapefile_detections/high/alaska/146_157_iwp/


### 2) IW Network validation dataset
https://par.nsf.gov/biblio/10554721-ice-wedge-network-centerline-ice-wedge-polygon-coverage-bernard-river-watershed-banks-island-canada


## 4. Products partial exhibition

* 230 Grids

![image](https://github.com/user-attachments/assets/75178f11-22ec-4721-8d0d-991a2a45e4b9)


* IWP count in Alaska

![image](https://github.com/user-attachments/assets/14f54b39-4d08-486b-967e-c20558da4a98)

## 5. References
Witharana, C., Bhuiyan, M. A. E., & Liljedahl, A. K. (2020). Big Imagery and High Performance Computing as Resources to Understand Changing Arctic Polygonal Tundra. The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences, 44, 111-116.

Udawalpola, M., Hasan, A., Liljedahl, A. K., Soliman, A., & Witharana, C. (2021). Operational-scale geoai for pan-arctic permafrost feature detection from high-resolution satellite imagery. The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences, 44, 175-180.

Liljedahl, A. K., Witharana, C., & Manos, E. (2024). The capillaries of the Arctic tundra. Nature Water, 2(7), 611-614.

Liljedahl, A. K., Boike, J., Daanen, R. P., Fedorov, A. N., Frost, G. V., Grosse, G., ... & Zona, D. (2016). Pan-Arctic ice-wedge degradation in warming permafrost and its influence on tundra hydrology. Nature geoscience, 9(4), 312-318.

