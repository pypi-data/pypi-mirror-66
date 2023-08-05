/*
 * Python object definition of the libfsntfs object identifier attribute
 *
 * Copyright (C) 2010-2020, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#if !defined( _PYFSNTFS_OBJECT_IDENTIFIER_ATTRIBUTE_H )
#define _PYFSNTFS_OBJECT_IDENTIFIER_ATTRIBUTE_H

#include <common.h>
#include <types.h>

#include "pyfsntfs_attribute.h"
#include "pyfsntfs_libfsntfs.h"
#include "pyfsntfs_python.h"

#if defined( __cplusplus )
extern "C" {
#endif

extern PyMethodDef pyfsntfs_object_identifier_attribute_object_methods[];
extern PyTypeObject pyfsntfs_object_identifier_attribute_type_object;

PyObject *pyfsntfs_object_identifier_attribute_get_droid_file_identifier(
           pyfsntfs_attribute_t *pyfsntfs_attribute,
           PyObject *arguments );

PyObject *pyfsntfs_object_identifier_attribute_get_birth_droid_volume_identifier(
           pyfsntfs_attribute_t *pyfsntfs_attribute,
           PyObject *arguments );

PyObject *pyfsntfs_object_identifier_attribute_get_birth_droid_file_identifier(
           pyfsntfs_attribute_t *pyfsntfs_attribute,
           PyObject *arguments );

PyObject *pyfsntfs_object_identifier_attribute_get_birth_droid_domain_identifier(
           pyfsntfs_attribute_t *pyfsntfs_attribute,
           PyObject *arguments );

#if defined( __cplusplus )
}
#endif

#endif /* !defined( _PYFSNTFS_OBJECT_IDENTIFIER_ATTRIBUTE_H ) */

