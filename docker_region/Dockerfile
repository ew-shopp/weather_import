FROM python:2
WORKDIR /weather

RUN pip install --no-cache-dir numpy 
RUN pip install --no-cache-dir https://software.ecmwf.int/wiki/download/attachments/56664858/ecmwf-api-client-python.tgz

# In order to install pygrib we first have to install matplotlib with basemap toolkit
RUN pip install --no-cache-dir matplotlib 
RUN wget https://github.com/matplotlib/basemap/archive/v1.1.0.tar.gz
RUN tar -xzf v1.1.0.tar.gz

# Basemap requires additional dependency geos whose source code is included in basemap
WORKDIR /weather/basemap-1.1.0/geos-3.3.3
ENV GEOS_DIR=/weather/geos/
RUN ./configure --prefix=$GEOS_DIR
RUN make; make install

# Now we can install basemap:
WORKDIR /weather/basemap-1.1.0
RUN python setup.py install
# Basemap requires pyproj 
RUN pip install --no-cache-dir pyproj 

# The next step is installation of GRIB API
RUN apt-get --yes update
RUN apt-get --yes install cmake

WORKDIR /weather/tmp
RUN wget -O grib_api-source.tar.gz https://software.ecmwf.int/wiki/download/attachments/3473437/grib_api-1.24.0-Source.tar.gz?api=v2
RUN tar -xzf grib_api-source.tar.gz
WORKDIR /weather/tmp/build
# Overwrite with modified file omitting FORTRAN
COPY CMakeLists.txt /weather/tmp/grib_api-1.24.0-Source
RUN cmake ../grib_api-1.24.0-Source -DCMAKE_INSTALL_PREFIX=/weather/grib_api/
RUN make; ctest; make install

# Pygrib installation
RUN apt-get --yes install unzip
COPY pygrib-master.zip /weather
WORKDIR /weather
RUN unzip pygrib-master.zip
# Overwrite with modified file with correct grib_api_dir
COPY setup.cfg /weather/pygrib-master
WORKDIR /weather/pygrib-master
RUN python setup.py build
RUN python setup.py install

# Weather lib installation
COPY weather-data-master.zip /weather
WORKDIR /weather
RUN unzip weather-data-master.zip
WORKDIR /weather/weather-data-master
RUN python setup.py install

RUN pip install --no-cache-dir pandas
RUN pip install --no-cache-dir geopy 

COPY ./py_app /weather/weather-data-master/weather_import
COPY ./bash_scripts /code

ENTRYPOINT ["/code/supervisor_sigterm.sh"]


