import numpy as np


def rotate_vector_about_vector(vector, about_vector, amount):
	"""
	Rotates a given vector about another vector.

	Implements Rodrigues' rotation formula:
	https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula

	Example:

	>>> rotate_vector_about_vector(np.array([1, 0, 1]), np.array([0, 0, 1]), np.pi)
	array([-1.0000000e+00,  1.2246468e-16,  1.0000000e+00])

	:param vector:
	:type vector:
	:param about_vector:
	:type about_vector:
	:param amount:
	:type amount:
	:return:
	:rtype:
	"""
	about_vector = about_vector / np.linalg.norm(about_vector)
	amount_rad = amount
	v_rot = vector * np.cos(amount_rad) \
			+ np.cross(about_vector, vector) \
			* np.sin(amount_rad) + about_vector \
			* np.dot(about_vector, vector) \
			* (1 - np.cos(amount_rad))

	return v_rot
