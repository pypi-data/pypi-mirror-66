
import numpy as np
import pandas as pd
from pathlib import Path





def calc_global_normal_vector(alfa, beta, bearing, inclination):      #input degrees
    alfa = np.deg2rad(alfa)                # Degrees to radians
    beta = np.deg2rad(beta)
    bearing = np.deg2rad(bearing)
    inclination = np.deg2rad(inclination)
                                                        # calculate normal vector of the fracture
    ng_1 = np.cos(np.pi / 2 - bearing) * np.cos(np.pi / 2 - inclination) * np.cos(beta) * np.cos(alfa) - np.sin(np.pi / 2 - bearing) * np.sin(beta) * np.cos(alfa) + np.cos(np.pi / 2 - bearing) * np.sin(np.pi / 2 - inclination) * np.sin(alfa)
    ng_2 = np.sin(np.pi / 2 - bearing) * np.cos(np.pi / 2 - inclination) * np.cos(beta) * np.cos(alfa) + np.cos(np.pi / 2 - bearing) * np.sin(beta) * np.cos(alfa) + np.sin(np.pi / 2 - bearing) * np.sin(np.pi / 2 - inclination) * np.sin(alfa)
    ng_3 = -np.sin(np.pi / 2 - inclination) * np.cos(beta) * np.cos(alfa) + np.cos(np.pi / 2 - inclination) * np.sin(alfa)

    return np.array([ng_1, ng_2, ng_3])            # return normal vector of the fracture

def calc_trend_plunge_from_vector(ng):


    ng = ng/np.linalg.norm(ng) # normalize vector
    nx = ng[0]
    ny = ng[1]
    nz = ng[2]

    if np.abs(nz) < 1:
            #        Check if the normal point upwards
      if nz > 0:
                      #invert the normal
         nz = -nz
                     #calculate and normalise the projection if the normal on the xy-plane
         xynx = -nx / ((nx ** 2 + ny ** 2) ** 0.5)
         xyny = -ny / ((nx ** 2 + ny ** 2) ** 0.5)
      else:
                      #calculate and normalise the projection if the normal on the xy-plane
         xynx = nx / ((nx ** 2 + ny ** 2) ** 0.5)
         xyny = ny / ((nx ** 2 + ny ** 2) ** 0.5)



                       #check if fracture is exactly south...
      if xynx >= 1:
         trend360 = 90

                        # or north striking or other orientation
      elif xynx <= -1:
         trend360 = 270

                        #Check if the y-component is negative
      elif xyny < 0:
         trend360 = 90 + np.rad2deg(np.arccos(xynx))
         if trend360 > 0:
             trend360 = trend360 - 360
      else:
         trend360 = 90 - np.rad2deg(np.arccos(xynx))
         if trend360 < 0:
             trend360 = trend360 + 360


                      #Calculate the plunge
      plunge360 = np.rad2deg(np.arcsin(-nz))

    else:
                        #The fracture is horizontal
          trend360 = 0
          plunge360 = 90
    return trend360, plunge360

def calc_real_result(trend360, plunge360):        # Due to differences in nomenclature, result must be changed a bit
    if trend360 > 180:
        trend = trend360 - 180
    else:
        trend = trend360 + 180
    plunge = 90-plunge360
    return plunge, trend

def calc_plunge_trend(alfa, beta, bearing, inclination):                   # Workflow of transforming
    inclination = -inclination
    ng = calc_global_normal_vector(alfa, beta, bearing, inclination)
    trend360, plunge360 = calc_trend_plunge_from_vector(ng)
    plunge, trend = calc_real_result(trend360, plunge360)
    return plunge, trend

def calc_plunge_and_trend_for_file(filename):                            # Reads file and saves new one with results
    df = pd.read_csv(filename, sep=';')
    # Creates and calculates new columns:
    df[['plunge', 'trend']] = df.apply(\
      lambda row: pd.Series(calc_plunge_trend(row['alfa'], row['beta'], row['bearing'], row['plunge'])), axis=1)
    savename = Path(filename).stem.split('.')[0]+'_orient_calculated.csv'    # Defines savename
    df.to_csv(savename, sep=';')              # Saves new .csv file



