"""
Dev module.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import sympy
from sympy import Plane, Point3D, Line3D
from sympy import symbols
import bisect
import configparser
import json
from pathlib import Path

from drillcore_transformations.transformations import transform_without_gamma, vector_from_dip_and_dir

def round_outputs(number):
	return round(number, 2)

def calc_normal_vector_of_plane(dip, dir):
	plane_vector_1 = vector_from_dip_and_dir(dip, dir)
	plane_vector_2 = vector_from_dip_and_dir(dip=0, dir=dir+90)
	plane_normal = np.cross(plane_vector_1, plane_vector_2)
	plane_normal = plane_normal if plane_normal[2] > 0 else -plane_normal
	return plane_normal / np.linalg.norm(plane_normal)


def calc_plane_dir_dip_old(normal):
	"""
	Calculate direction of dip and dip of a plane based on normal vector of plane.

	:param normal: Normal vector of a plane.
	:type normal: numpy.ndarray
	:return: Direction of dip and dip in degrees
	:rtype: tuple[float, float]
	"""
	# Fracture vector plane plunge
	measured_plane = Plane(Point3D(0, 0, 0), normal_vector=tuple(normal))
	surface_plane = Plane(Point3D(0, 0, 0), Point3D(1, 1, 0), Point3D(1, -1, 0))
	dip_radians = measured_plane.angle_between(surface_plane)
	dip_degrees = \
		np.rad2deg(float(dip_radians)) \
			if np.rad2deg(float(dip_radians)) <= 90 else \
			180 - np.rad2deg(float(dip_radians))

	# Get fracture vector trend from fracture normal vector
	normal_projection = surface_plane.projection_line(Line3D(Point3D(0, 0, 0), direction_ratio=tuple(normal)))
	north_line = Line3D(Point3D(0, 0, 0), Point3D(0, 1, 0))
	# y is negative
	if float(normal_projection.p2[1]) < 0:
		# x is negative
		if float(normal_projection.p2[0]) < 0:
			dir_radians = sympy.pi + normal_projection.smallest_angle_between(north_line)
		# x is positive
		else:
			dir_radians = sympy.pi - normal_projection.smallest_angle_between(north_line)
	# y is positive
	else:
		# x is negative
		if float(normal_projection.p2[0]) < 0:
			dir_radians = 2 * sympy.pi - normal_projection.smallest_angle_between(north_line)
		# x is positive
		else:
			dir_radians = normal_projection.smallest_angle_between(north_line)

	dir_degrees = np.rad2deg(float(dir_radians))
	return dir_degrees, dip_degrees

def trend_plunge_of_vector(vector):
	"""
	Calculate trend and plunge of a vector.

	:param vector: Vector
	:type vector: numpy.ndarray
	:return: Trend and plunge
	:rtype: tuple[float, float]
	"""
	# Get vector trend from plane normal vector
	surface_plane = Plane(Point3D(0, 0, 0), Point3D(1, 1, 0), Point3D(1, -1, 0))
	vector_projection = surface_plane.projection_line(Line3D(Point3D(0, 0, 0), direction_ratio=tuple(vector)))
	north_line = Line3D(Point3D(0, 0, 0), Point3D(0, 1, 0))
	# y is negative
	if float(vector_projection.p2[1]) < 0:
		# x is negative
		if float(vector_projection.p2[0]) < 0:
			trend_radians = sympy.pi + vector_projection.smallest_angle_between(north_line)
		# x is positive
		else:
			trend_radians = sympy.pi - vector_projection.smallest_angle_between(north_line)
	# y is positive
	else:
		# x is negative
		if float(vector_projection.p2[0]) < 0:
			trend_radians = 2 * sympy.pi - vector_projection.smallest_angle_between(north_line)
		# x is positive
		else:
			trend_radians = vector_projection.smallest_angle_between(north_line)

	trend_degrees = np.rad2deg(float(trend_radians))
	plunge_degrees = np.rad2deg(-np.arcsin(vector[2]))

	return trend_degrees, plunge_degrees

def trend_plunge_of_vector_old(vector):
	"""
	Calculate trend and plunge of a vector.

	:param vector: Vector
	:type vector: numpy.ndarray
	:return: Trend and plunge
	:rtype: tuple[float, float]
	"""
	# Get vector trend from plane normal vector
	surface_plane = Plane(Point3D(0, 0, 0), Point3D(1, 1, 0), Point3D(1, -1, 0))
	vector_projection = surface_plane.projection_line(Line3D(Point3D(0, 0, 0), direction_ratio=tuple(vector)))
	north_line = Line3D(Point3D(0, 0, 0), Point3D(0, 1, 0))
	# y is negative
	if float(vector_projection.p2[1]) < 0:
		# x is negative
		if float(vector_projection.p2[0]) < 0:
			trend_radians = sympy.pi + vector_projection.smallest_angle_between(north_line)
		# x is positive
		else:
			trend_radians = sympy.pi - vector_projection.smallest_angle_between(north_line)
	# y is positive
	else:
		# x is negative
		if float(vector_projection.p2[0]) < 0:
			trend_radians = 2 * sympy.pi - vector_projection.smallest_angle_between(north_line)
		# x is positive
		else:
			trend_radians = vector_projection.smallest_angle_between(north_line)

	trend_degrees = np.rad2deg(float(trend_radians))
	plunge_degrees = np.rad2deg(-np.arcsin(vector[2]))

	return trend_degrees, plunge_degrees

def transform_excel_with_depth(measurement_filename, depth_filename):
	measurements = pd.read_excel(measurement_filename)
	depth = pd.read_excel(depth_filename)
	trend_plunge = []
	for idx, row in measurements.iterrows():
		val = row["LENGTH_FROM"]
		right = bisect.bisect(depth["DEPTH"].values, val)
		if right == len(depth):
			right = right - 1
		# Check if index is -1 in which case right and left both work. Depth must be ordered!
		left = right - 1 if right - 1 != -1 else right

		# Check which is closer, left or right to value.
		take = right if depth["DEPTH"].iloc[right] - val <= val - depth["DEPTH"].iloc[left] else left
		trend, plunge = depth[["AZIMUTH", "DIP"]].iloc[take]
		plunge = -plunge
		trend_plunge.append((trend, plunge))
	# TODO: Use zip
	measurements["borehole_trend"], measurements["borehole_plunge"] = \
		[tr[0] for tr in trend_plunge], [tr[1] for tr in trend_plunge]

	# ALPHA must be reversed to achieve correct result.
	measurements[['plane_dip', 'plane_dir']] = measurements.apply(
		lambda row: pd.Series(transform_without_gamma(
			-row['ALPHA_CORE'], row['BETA_CORE'], row['borehole_trend'], row['borehole_plunge'])), axis=1)
	measurements[['plane_dip', 'plane_dir']] = \
		measurements[['plane_dip', 'plane_dir']].applymap(round_outputs)

	measurements["DIR_ERROR"] = abs(measurements["DIR_CORE"] - measurements["plane_dir"])
	measurements["DIP_ERROR"] = abs(measurements["DIP_CORE"] - measurements["plane_dip"])

	measurements["NORMAL_CORE"] = measurements.apply(lambda row: calc_normal_vector_of_plane(row["DIP_CORE"], row["DIR_CORE"]), axis=1)
	measurements["NORMAL_plane"] = measurements.apply(lambda row: calc_normal_vector_of_plane(row["plane_dip"], row["plane_dir"]), axis=1)

	measurements["NORMAL_DOT"] = measurements.apply(lambda row: np.dot(row["NORMAL_CORE"], row["NORMAL_plane"]), axis=1)

	measurements["NORMAL_ERROR"] = measurements["NORMAL_DOT"].apply(np.arccos)
	measurements["NORMAL_ERROR_DEG"] = measurements["NORMAL_ERROR"].apply(np.rad2deg)

	measurements.to_csv(r"F:\Users\nikke\Desktop\olkiluoto_data\KR55_raot_newcalc_with_errors_normal.csv", mode="w+", sep=";")

def initialize_config_dev():
	"""
	Creates a configfile with default names for alpha, beta, etc. Filename will be config.ini. Manual editing
	of this file is allowed but editing methods are also present for adding column names.
	"""
	config = configparser.ConfigParser()

	# Measurement file
	config["MEASUREMENTS"] = {}
	config["MEASUREMENTS"]["ALPHA"] = json.dumps(["ALPHA", "alpha", "ALPHA_CORE"])
	config["MEASUREMENTS"]["BETA"] = json.dumps(["BETA", "beta", "BETA_CORE"])
	config["MEASUREMENTS"]["GAMMA"] = json.dumps(["GAMMA", "gamma", "GAMMA_CORE"])
	config["MEASUREMENTS"]["MEASUREMENT_DEPTH"] = json.dumps(["MEASUREMENT_DEPTH", "measurement_depth", "LENGTH_FROM"
																 , "LENGTH_IMAGE"])

	# Depth file
	config["DEPTHS"] = {}
	config["DEPTHS"]["DEPTH"] = json.dumps(["DEPTH", "depth"])

	# Borehole trend and plunge
	config["BOREHOLE"] = {}
	config["BOREHOLE"]["BOREHOLE_TREND"] = json.dumps(["BOREHOLE_TREND", "borehole_trend", "AZIMUTH"])
	config["BOREHOLE"]["BOREHOLE_PLUNGE"] = json.dumps(["BOREHOLE_PLUNGE", "borehole_plunge", "INCLINATION", "inclination"])

	# Write to .ini file. Will overwrite old one or make a new one.
	with open("config.ini", "w+") as configfile:
		config.write(configfile)


def add_column_name(header, base_column, name):
	"""
	Method for adding a column name to recognize measurement type. E.g. if your alpha measurements are in a column
	that is named "alpha_measurements" you can add it to the config.ini file with:

	>>>add_column_name("MEASUREMENTS", "ALPHA", "alpha_measurements")

	:param header: You may add new column names to the measurements file and to the file containing measurement depth
		information.
	:type header: str
	:param base_column: Which type of measurement is the column name.
		Base types for measurements are:
		"ALPHA" "BETA" "GAMMA" "MEASUREMENT_DEPTH"
		Base types for depths are:
		"DEPTH"
		Base types for borehole are:
		"BOREHOLE_TREND" "BOREHOLE_PLUNGE"
	:type base_column: str
	:param name: Name of the new column you want to add.
	:type name: str
	"""
	assert header in ["MEASUREMENTS", "DEPTHS"]
	config = configparser.ConfigParser()
	configname = "config.ini"
	if not Path(configname).exists():
		print("config.ini configfile not found. Making a new one with default values.")
		initialize_config_dev()
	assert Path(configname).exists()
	config.read(configname)
	column_list = json.loads(config.get(header, base_column))

	assert isinstance(column_list, list)
	column_list.append(name)
	config[header][base_column] = json.dumps(column_list)
	save_config(config)


def save_config(config):
	# Write to .ini file. Will overwrite or make a new one.
	with open("config.ini", "w+") as configfile:
		config.write(configfile)


def main():
	from drillcore_transformations.usage import initialize_config, transform_excel_two_files, add_column_name, convention_testing_csv
	# mes_file = r"F:\Users\nikke\Desktop\olkiluoto_data\KR55_raot.xlsx"
	# dep_file = r"F:\Users\nikke\Desktop\olkiluoto_data\KR55_taipuma.xlsx"
	# initialize_config()
	# add_column_name("BOREHOLE", "borehole_plunge", "DIP")
	# transform_excel_two_files(mes_file, dep_file, False, output="asdfile.csv")

	filename = r"F:\Users\nikke\PycharmProjects\drillcore_transformation\drillcore_transformations\sample_data\Logging_sheet.csv"
	convention_testing_csv(filename, with_gamma=True, visualize=False, output=r"F:\Users\nikke\temp\file.csv", img_dir=r"F:\Users\nikke\temp")

if __name__ == "__main__":
	main()






