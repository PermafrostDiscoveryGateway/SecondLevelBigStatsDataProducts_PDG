# Second-level big statistics data products for Ice Wedge Polygon (IWP) across Pan-Arctic
Generate a second-level statistics data products based on the IWP dataset from PDG


-------------------------------
## Repository Structure
1. `tutorials/`: Step-by-step guides and detailed progress documentation. This foloder contains all the detailed progresses we have done to produce this big data product along the project. It consists of three python files that introduce every step to generate results.

   **short_tutorial.pdf:A step-by-step tutorial to generate current IWP stats maps.**

   long_tutorial.pdf: The entire progress track along the project meetings.

   **gpkg_statstistics_mapping_noDatabase_alaska.ipynb: the code using geopackages to generate current big stats maps. (This is what we use currently.)**

   shapefile_CountMap.ipynb: the code using shapefile to generate only count maps.

   shapefile_CoverageMap.ipynb: the code using shapefile to generate coverage heat maps.



3. `data/`: Sample datasets and generated results, primarily focusing on the Alaska region. This folder contains the part of the results we have generated in Alaska region.
   This folder contains part of final stats: IWP count, IWP area, length (diameter) sum/max/min/median/mean/perimeter, width, LCP count.
  
4. `src/`: Core scripts for data processing and map generation. This foloder contains two sub project:

   1) using geopackages.

      **statistics_mapping_noDatabase.py (Without database. This is what we use currently): This is the code we are currently use for generating data products. It runs without database to achieve the best performance.**

      statistics_mapping.py (With database): This is previous experiments we've tried.

   3) using shapefile.
  
      Countmap.py: This file we used to create IWP count (heatmap) map based on shapefile.

      CoveragePercentage.py: This file we used to create coverage ratio map based on shapefile.

      createSQL.sh & shpImport.sh: These shell files were created to be used by the above two files in python.

-------------------------------



## Prerequisites

- Python 3.7 or higher

- Recommended to use a virtual environment


## Installation
### 1) Clone the repository:

   ```bash
   git clone https://github.com/ASUcicilab/Second-level-Big-Stats-Data-Products.git
   cd Second-level-Big-Stats-Data-Products
   ```

### 2) Create and activate a virtual environment:

You can create either using pip or conda based on the running environment. This is an example using pip.

   ```python3 -m venv tutorial-venv```
   ```source venv/bin/activate```

### 3) Install required python packages

   ```pip install -r requirements.txt```


-------------------------------



## 🚀 Getting Started

## 1. Project objectives
Ice Wedge (IW) is a crack in the ground formed by a narrow or thin piece of ice that measures up to 3–4 meters in length at ground level. As IW gets deeper, Ice Wedge Polygons are formed. 

The large number of IWPs across the entire Pan-Arctic region were extracted and organized by PDG (either in geopackage or shapefile format in an arctic projection EPSG:3413).

The goal of this project is to analysis the polygons, and generate data products to describe different statistical profiles of IWP. This include: 

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

### What we have done

1) First-level IWP vector data [Witharana et al. (2020) and Udawalpola (2021)].

2) Run Prithivi on the first-level data.


### What we are doing

1) Create second-level IWP stats data based on the first-level data.


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


### 4.1. Product value meaning

1) Value -1 means there are no IWPs calculated in this pixel.
2) Value -99 means there is an outlier of oversized IWP geopackages when downloading.


## 5. References
Witharana, C., Bhuiyan, M. A. E., & Liljedahl, A. K. (2020). Big Imagery and High Performance Computing as Resources to Understand Changing Arctic Polygonal Tundra. The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences, 44, 111-116.

Udawalpola, M., Hasan, A., Liljedahl, A. K., Soliman, A., & Witharana, C. (2021). Operational-scale geoai for pan-arctic permafrost feature detection from high-resolution satellite imagery. The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences, 44, 175-180.

Liljedahl, A. K., Witharana, C., & Manos, E. (2024). The capillaries of the Arctic tundra. Nature Water, 2(7), 611-614.

Liljedahl, A. K., Boike, J., Daanen, R. P., Fedorov, A. N., Frost, G. V., Grosse, G., ... & Zona, D. (2016). Pan-Arctic ice-wedge degradation in warming permafrost and its influence on tundra hydrology. Nature geoscience, 9(4), 312-318.

