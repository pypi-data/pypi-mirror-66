/*
 * Library mft_metadata_file type test program
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

#include <common.h>
#include <file_stream.h>
#include <narrow_string.h>
#include <system_string.h>
#include <types.h>
#include <wide_string.h>

#if defined( HAVE_STDLIB_H ) || defined( WINAPI )
#include <stdlib.h>
#endif

#include "fsntfs_test_functions.h"
#include "fsntfs_test_getopt.h"
#include "fsntfs_test_libbfio.h"
#include "fsntfs_test_libcerror.h"
#include "fsntfs_test_libclocale.h"
#include "fsntfs_test_libfsntfs.h"
#include "fsntfs_test_libuna.h"
#include "fsntfs_test_macros.h"
#include "fsntfs_test_memory.h"

#include "../libfsntfs/libfsntfs_mft_metadata_file.h"

#if defined( HAVE_WIDE_SYSTEM_CHARACTER ) && SIZEOF_WCHAR_T != 2 && SIZEOF_WCHAR_T != 4
#error Unsupported size of wchar_t
#endif

/* Define to make fsntfs_test_mft_metadata_file generate verbose output
#define FSNTFS_TEST_MFT_METADATA_FILE_VERBOSE
 */

#if !defined( LIBFSNTFS_HAVE_BFIO )

LIBFSNTFS_EXTERN \
int libfsntfs_check_mft_metadata_file_signature_file_io_handle(
     libbfio_handle_t *file_io_handle,
     libfsntfs_error_t **error );

#endif /* !defined( LIBFSNTFS_HAVE_BFIO ) */

/* Creates and opens a source MFT metadata file
 * Returns 1 if successful or -1 on error
 */
int fsntfs_test_mft_metadata_file_open_source(
     libfsntfs_mft_metadata_file_t **mft_metadata_file,
     libbfio_handle_t *file_io_handle,
     libcerror_error_t **error )
{
	static char *function = "fsntfs_test_mft_metadata_file_open_source";
	int result            = 0;

	if( mft_metadata_file == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid MFT metadata file.",
		 function );

		return( -1 );
	}
	if( file_io_handle == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid file IO handle.",
		 function );

		return( -1 );
	}
	if( libfsntfs_mft_metadata_file_initialize(
	     mft_metadata_file,
	     error ) != 1 )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_INITIALIZE_FAILED,
		 "%s: unable to initialize MFT metadata file.",
		 function );

		goto on_error;
	}
	result = libfsntfs_mft_metadata_file_open_file_io_handle(
	          *mft_metadata_file,
	          file_io_handle,
	          LIBFSNTFS_OPEN_READ,
	          error );

	if( result != 1 )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_IO,
		 LIBCERROR_IO_ERROR_OPEN_FAILED,
		 "%s: unable to open MFT metadata file.",
		 function );

		goto on_error;
	}
	return( 1 );

on_error:
	if( *mft_metadata_file != NULL )
	{
		libfsntfs_mft_metadata_file_free(
		 mft_metadata_file,
		 NULL );
	}
	return( -1 );
}

/* Closes and frees a source MFT metadata file
 * Returns 1 if successful or -1 on error
 */
int fsntfs_test_mft_metadata_file_close_source(
     libfsntfs_mft_metadata_file_t **mft_metadata_file,
     libcerror_error_t **error )
{
	static char *function = "fsntfs_test_mft_metadata_file_close_source";
	int result            = 0;

	if( mft_metadata_file == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid MFT metadata file.",
		 function );

		return( -1 );
	}
	if( libfsntfs_mft_metadata_file_close(
	     *mft_metadata_file,
	     error ) != 0 )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_IO,
		 LIBCERROR_IO_ERROR_CLOSE_FAILED,
		 "%s: unable to close MFT metadata file.",
		 function );

		result = -1;
	}
	if( libfsntfs_mft_metadata_file_free(
	     mft_metadata_file,
	     error ) != 1 )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_FINALIZE_FAILED,
		 "%s: unable to free MFT metadata file.",
		 function );

		result = -1;
	}
	return( result );
}

/* Tests the libfsntfs_mft_metadata_file_initialize function
 * Returns 1 if successful or 0 if not
 */
int fsntfs_test_mft_metadata_file_initialize(
     void )
{
	libcerror_error_t *error                         = NULL;
	libfsntfs_mft_metadata_file_t *mft_metadata_file = NULL;
	int result                                       = 0;

#if defined( HAVE_FSNTFS_TEST_MEMORY )
	int number_of_malloc_fail_tests                  = 1;
	int number_of_memset_fail_tests                  = 1;
	int test_number                                  = 0;
#endif

	/* Test regular cases
	 */
	result = libfsntfs_mft_metadata_file_initialize(
	          &mft_metadata_file,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	FSNTFS_TEST_ASSERT_IS_NOT_NULL(
	 "mft_metadata_file",
	 mft_metadata_file );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	result = libfsntfs_mft_metadata_file_free(
	          &mft_metadata_file,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "mft_metadata_file",
	 mft_metadata_file );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test error cases
	 */
	result = libfsntfs_mft_metadata_file_initialize(
	          NULL,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	FSNTFS_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	mft_metadata_file = (libfsntfs_mft_metadata_file_t *) 0x12345678UL;

	result = libfsntfs_mft_metadata_file_initialize(
	          &mft_metadata_file,
	          &error );

	mft_metadata_file = NULL;

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	FSNTFS_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

#if defined( HAVE_FSNTFS_TEST_MEMORY )

	for( test_number = 0;
	     test_number < number_of_malloc_fail_tests;
	     test_number++ )
	{
		/* Test libfsntfs_mft_metadata_file_initialize with malloc failing
		 */
		fsntfs_test_malloc_attempts_before_fail = test_number;

		result = libfsntfs_mft_metadata_file_initialize(
		          &mft_metadata_file,
		          &error );

		if( fsntfs_test_malloc_attempts_before_fail != -1 )
		{
			fsntfs_test_malloc_attempts_before_fail = -1;

			if( mft_metadata_file != NULL )
			{
				libfsntfs_mft_metadata_file_free(
				 &mft_metadata_file,
				 NULL );
			}
		}
		else
		{
			FSNTFS_TEST_ASSERT_EQUAL_INT(
			 "result",
			 result,
			 -1 );

			FSNTFS_TEST_ASSERT_IS_NULL(
			 "mft_metadata_file",
			 mft_metadata_file );

			FSNTFS_TEST_ASSERT_IS_NOT_NULL(
			 "error",
			 error );

			libcerror_error_free(
			 &error );
		}
	}
	for( test_number = 0;
	     test_number < number_of_memset_fail_tests;
	     test_number++ )
	{
		/* Test libfsntfs_mft_metadata_file_initialize with memset failing
		 */
		fsntfs_test_memset_attempts_before_fail = test_number;

		result = libfsntfs_mft_metadata_file_initialize(
		          &mft_metadata_file,
		          &error );

		if( fsntfs_test_memset_attempts_before_fail != -1 )
		{
			fsntfs_test_memset_attempts_before_fail = -1;

			if( mft_metadata_file != NULL )
			{
				libfsntfs_mft_metadata_file_free(
				 &mft_metadata_file,
				 NULL );
			}
		}
		else
		{
			FSNTFS_TEST_ASSERT_EQUAL_INT(
			 "result",
			 result,
			 -1 );

			FSNTFS_TEST_ASSERT_IS_NULL(
			 "mft_metadata_file",
			 mft_metadata_file );

			FSNTFS_TEST_ASSERT_IS_NOT_NULL(
			 "error",
			 error );

			libcerror_error_free(
			 &error );
		}
	}
#endif /* defined( HAVE_FSNTFS_TEST_MEMORY ) */

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	if( mft_metadata_file != NULL )
	{
		libfsntfs_mft_metadata_file_free(
		 &mft_metadata_file,
		 NULL );
	}
	return( 0 );
}

/* Tests the libfsntfs_mft_metadata_file_free function
 * Returns 1 if successful or 0 if not
 */
int fsntfs_test_mft_metadata_file_free(
     void )
{
	libcerror_error_t *error = NULL;
	int result               = 0;

	/* Test error cases
	 */
	result = libfsntfs_mft_metadata_file_free(
	          NULL,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	FSNTFS_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	return( 0 );
}

/* Tests the libfsntfs_mft_metadata_file_open function
 * Returns 1 if successful or 0 if not
 */
int fsntfs_test_mft_metadata_file_open(
     const system_character_t *source )
{
	char narrow_source[ 256 ];

	libcerror_error_t *error                         = NULL;
	libfsntfs_mft_metadata_file_t *mft_metadata_file = NULL;
	int result                                       = 0;

	/* Initialize test
	 */
	result = fsntfs_test_get_narrow_source(
	          source,
	          narrow_source,
	          256,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	result = libfsntfs_mft_metadata_file_initialize(
	          &mft_metadata_file,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	FSNTFS_TEST_ASSERT_IS_NOT_NULL(
	 "mft_metadata_file",
	 mft_metadata_file );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test open
	 */
	result = libfsntfs_mft_metadata_file_open(
	          mft_metadata_file,
	          narrow_source,
	          LIBFSNTFS_OPEN_READ,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test error cases
	 */
	result = libfsntfs_mft_metadata_file_open(
	          mft_metadata_file,
	          narrow_source,
	          LIBFSNTFS_OPEN_READ,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	FSNTFS_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	/* Clean up
	 */
	result = libfsntfs_mft_metadata_file_free(
	          &mft_metadata_file,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "mft_metadata_file",
	 mft_metadata_file );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	if( mft_metadata_file != NULL )
	{
		libfsntfs_mft_metadata_file_free(
		 &mft_metadata_file,
		 NULL );
	}
	return( 0 );
}

#if defined( HAVE_WIDE_CHARACTER_TYPE )

/* Tests the libfsntfs_mft_metadata_file_open_wide function
 * Returns 1 if successful or 0 if not
 */
int fsntfs_test_mft_metadata_file_open_wide(
     const system_character_t *source )
{
	wchar_t wide_source[ 256 ];

	libcerror_error_t *error                         = NULL;
	libfsntfs_mft_metadata_file_t *mft_metadata_file = NULL;
	int result                                       = 0;

	/* Initialize test
	 */
	result = fsntfs_test_get_wide_source(
	          source,
	          wide_source,
	          256,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	result = libfsntfs_mft_metadata_file_initialize(
	          &mft_metadata_file,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	FSNTFS_TEST_ASSERT_IS_NOT_NULL(
	 "mft_metadata_file",
	 mft_metadata_file );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test open
	 */
	result = libfsntfs_mft_metadata_file_open_wide(
	          mft_metadata_file,
	          wide_source,
	          LIBFSNTFS_OPEN_READ,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test error cases
	 */
	result = libfsntfs_mft_metadata_file_open_wide(
	          mft_metadata_file,
	          wide_source,
	          LIBFSNTFS_OPEN_READ,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	FSNTFS_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	/* Clean up
	 */
	result = libfsntfs_mft_metadata_file_free(
	          &mft_metadata_file,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "mft_metadata_file",
	 mft_metadata_file );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	if( mft_metadata_file != NULL )
	{
		libfsntfs_mft_metadata_file_free(
		 &mft_metadata_file,
		 NULL );
	}
	return( 0 );
}

#endif /* defined( HAVE_WIDE_CHARACTER_TYPE ) */

/* Tests the libfsntfs_mft_metadata_file_close function
 * Returns 1 if successful or 0 if not
 */
int fsntfs_test_mft_metadata_file_close(
     void )
{
	libcerror_error_t *error = NULL;
	int result               = 0;

	/* Test error cases
	 */
	result = libfsntfs_mft_metadata_file_close(
	          NULL,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	FSNTFS_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	return( 0 );
}

/* Tests the libfsntfs_mft_metadata_file_open and libfsntfs_mft_metadata_file_close functions
 * Returns 1 if successful or 0 if not
 */
int fsntfs_test_mft_metadata_file_open_close(
     const system_character_t *source )
{
	libcerror_error_t *error                         = NULL;
	libfsntfs_mft_metadata_file_t *mft_metadata_file = NULL;
	int result                                       = 0;

	/* Initialize test
	 */
	result = libfsntfs_mft_metadata_file_initialize(
	          &mft_metadata_file,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	FSNTFS_TEST_ASSERT_IS_NOT_NULL(
	 "mft_metadata_file",
	 mft_metadata_file );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test open and close
	 */
#if defined( HAVE_WIDE_SYSTEM_CHARACTER )
	result = libfsntfs_mft_metadata_file_open_wide(
	          mft_metadata_file,
	          source,
	          LIBFSNTFS_OPEN_READ,
	          &error );
#else
	result = libfsntfs_mft_metadata_file_open(
	          mft_metadata_file,
	          source,
	          LIBFSNTFS_OPEN_READ,
	          &error );
#endif

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	result = libfsntfs_mft_metadata_file_close(
	          mft_metadata_file,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 0 );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test open and close a second time to validate clean up on close
	 */
#if defined( HAVE_WIDE_SYSTEM_CHARACTER )
	result = libfsntfs_mft_metadata_file_open_wide(
	          mft_metadata_file,
	          source,
	          LIBFSNTFS_OPEN_READ,
	          &error );
#else
	result = libfsntfs_mft_metadata_file_open(
	          mft_metadata_file,
	          source,
	          LIBFSNTFS_OPEN_READ,
	          &error );
#endif

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	result = libfsntfs_mft_metadata_file_close(
	          mft_metadata_file,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 0 );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Clean up
	 */
	result = libfsntfs_mft_metadata_file_free(
	          &mft_metadata_file,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "mft_metadata_file",
	 mft_metadata_file );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	if( mft_metadata_file != NULL )
	{
		libfsntfs_mft_metadata_file_free(
		 &mft_metadata_file,
		 NULL );
	}
	return( 0 );
}

/* Tests the libfsntfs_mft_metadata_file_signal_abort function
 * Returns 1 if successful or 0 if not
 */
int fsntfs_test_mft_metadata_file_signal_abort(
     libfsntfs_mft_metadata_file_t *mft_metadata_file )
{
	libcerror_error_t *error = NULL;
	int result               = 0;

	/* Test regular cases
	 */
	result = libfsntfs_mft_metadata_file_signal_abort(
	          mft_metadata_file,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test error cases
	 */
	result = libfsntfs_mft_metadata_file_signal_abort(
	          NULL,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	FSNTFS_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	return( 0 );
}

/* Tests the libfsntfs_mft_metadata_file_get_utf8_volume_name_size function
 * Returns 1 if successful or 0 if not
 */
int fsntfs_test_mft_metadata_file_get_utf8_volume_name_size(
     libfsntfs_mft_metadata_file_t *mft_metadata_file )
{
	libcerror_error_t *error         = NULL;
	size_t utf8_volume_name_size     = 0;
	int result                       = 0;
	int utf8_volume_name_size_is_set = 0;

	/* Test regular cases
	 */
	result = libfsntfs_mft_metadata_file_get_utf8_volume_name_size(
	          mft_metadata_file,
	          &utf8_volume_name_size,
	          &error );

	FSNTFS_TEST_ASSERT_NOT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	utf8_volume_name_size_is_set = result;

	/* Test error cases
	 */
	result = libfsntfs_mft_metadata_file_get_utf8_volume_name_size(
	          NULL,
	          &utf8_volume_name_size,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	FSNTFS_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	if( utf8_volume_name_size_is_set != 0 )
	{
		result = libfsntfs_mft_metadata_file_get_utf8_volume_name_size(
		          mft_metadata_file,
		          NULL,
		          &error );

		FSNTFS_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 -1 );

		FSNTFS_TEST_ASSERT_IS_NOT_NULL(
		 "error",
		 error );

		libcerror_error_free(
		 &error );
	}
	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	return( 0 );
}

/* Tests the libfsntfs_mft_metadata_file_get_utf8_volume_name function
 * Returns 1 if successful or 0 if not
 */
int fsntfs_test_mft_metadata_file_get_utf8_volume_name(
     libfsntfs_mft_metadata_file_t *mft_metadata_file )
{
	uint8_t utf8_volume_name[ 512 ];

	libcerror_error_t *error    = NULL;
	int result                  = 0;
	int utf8_volume_name_is_set = 0;

	/* Test regular cases
	 */
	result = libfsntfs_mft_metadata_file_get_utf8_volume_name(
	          mft_metadata_file,
	          utf8_volume_name,
	          512,
	          &error );

	FSNTFS_TEST_ASSERT_NOT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	utf8_volume_name_is_set = result;

	/* Test error cases
	 */
	result = libfsntfs_mft_metadata_file_get_utf8_volume_name(
	          NULL,
	          utf8_volume_name,
	          512,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	FSNTFS_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	if( utf8_volume_name_is_set != 0 )
	{
		result = libfsntfs_mft_metadata_file_get_utf8_volume_name(
		          mft_metadata_file,
		          NULL,
		          512,
		          &error );

		FSNTFS_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 -1 );

		FSNTFS_TEST_ASSERT_IS_NOT_NULL(
		 "error",
		 error );

		libcerror_error_free(
		 &error );

		result = libfsntfs_mft_metadata_file_get_utf8_volume_name(
		          mft_metadata_file,
		          utf8_volume_name,
		          0,
		          &error );

		FSNTFS_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 -1 );

		FSNTFS_TEST_ASSERT_IS_NOT_NULL(
		 "error",
		 error );

		libcerror_error_free(
		 &error );

		result = libfsntfs_mft_metadata_file_get_utf8_volume_name(
		          mft_metadata_file,
		          utf8_volume_name,
		          (size_t) SSIZE_MAX + 1,
		          &error );

		FSNTFS_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 -1 );

		FSNTFS_TEST_ASSERT_IS_NOT_NULL(
		 "error",
		 error );

		libcerror_error_free(
		 &error );
	}
	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	return( 0 );
}

/* Tests the libfsntfs_mft_metadata_file_get_utf16_volume_name_size function
 * Returns 1 if successful or 0 if not
 */
int fsntfs_test_mft_metadata_file_get_utf16_volume_name_size(
     libfsntfs_mft_metadata_file_t *mft_metadata_file )
{
	libcerror_error_t *error          = NULL;
	size_t utf16_volume_name_size     = 0;
	int result                        = 0;
	int utf16_volume_name_size_is_set = 0;

	/* Test regular cases
	 */
	result = libfsntfs_mft_metadata_file_get_utf16_volume_name_size(
	          mft_metadata_file,
	          &utf16_volume_name_size,
	          &error );

	FSNTFS_TEST_ASSERT_NOT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	utf16_volume_name_size_is_set = result;

	/* Test error cases
	 */
	result = libfsntfs_mft_metadata_file_get_utf16_volume_name_size(
	          NULL,
	          &utf16_volume_name_size,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	FSNTFS_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	if( utf16_volume_name_size_is_set != 0 )
	{
		result = libfsntfs_mft_metadata_file_get_utf16_volume_name_size(
		          mft_metadata_file,
		          NULL,
		          &error );

		FSNTFS_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 -1 );

		FSNTFS_TEST_ASSERT_IS_NOT_NULL(
		 "error",
		 error );

		libcerror_error_free(
		 &error );
	}
	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	return( 0 );
}

/* Tests the libfsntfs_mft_metadata_file_get_utf16_volume_name function
 * Returns 1 if successful or 0 if not
 */
int fsntfs_test_mft_metadata_file_get_utf16_volume_name(
     libfsntfs_mft_metadata_file_t *mft_metadata_file )
{
	uint16_t utf16_volume_name[ 512 ];

	libcerror_error_t *error     = NULL;
	int result                   = 0;
	int utf16_volume_name_is_set = 0;

	/* Test regular cases
	 */
	result = libfsntfs_mft_metadata_file_get_utf16_volume_name(
	          mft_metadata_file,
	          utf16_volume_name,
	          512,
	          &error );

	FSNTFS_TEST_ASSERT_NOT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	utf16_volume_name_is_set = result;

	/* Test error cases
	 */
	result = libfsntfs_mft_metadata_file_get_utf16_volume_name(
	          NULL,
	          utf16_volume_name,
	          512,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	FSNTFS_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	if( utf16_volume_name_is_set != 0 )
	{
		result = libfsntfs_mft_metadata_file_get_utf16_volume_name(
		          mft_metadata_file,
		          NULL,
		          512,
		          &error );

		FSNTFS_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 -1 );

		FSNTFS_TEST_ASSERT_IS_NOT_NULL(
		 "error",
		 error );

		libcerror_error_free(
		 &error );

		result = libfsntfs_mft_metadata_file_get_utf16_volume_name(
		          mft_metadata_file,
		          utf16_volume_name,
		          0,
		          &error );

		FSNTFS_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 -1 );

		FSNTFS_TEST_ASSERT_IS_NOT_NULL(
		 "error",
		 error );

		libcerror_error_free(
		 &error );

		result = libfsntfs_mft_metadata_file_get_utf16_volume_name(
		          mft_metadata_file,
		          utf16_volume_name,
		          (size_t) SSIZE_MAX + 1,
		          &error );

		FSNTFS_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 -1 );

		FSNTFS_TEST_ASSERT_IS_NOT_NULL(
		 "error",
		 error );

		libcerror_error_free(
		 &error );
	}
	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	return( 0 );
}

/* Tests the libfsntfs_mft_metadata_file_get_number_of_file_entries function
 * Returns 1 if successful or 0 if not
 */
int fsntfs_test_mft_metadata_file_get_number_of_file_entries(
     libfsntfs_mft_metadata_file_t *mft_metadata_file )
{
	libcerror_error_t *error          = NULL;
	uint64_t number_of_file_entries   = 0;
	int number_of_file_entries_is_set = 0;
	int result                        = 0;

	/* Test regular cases
	 */
	result = libfsntfs_mft_metadata_file_get_number_of_file_entries(
	          mft_metadata_file,
	          &number_of_file_entries,
	          &error );

	FSNTFS_TEST_ASSERT_NOT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	FSNTFS_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	number_of_file_entries_is_set = result;

	/* Test error cases
	 */
	result = libfsntfs_mft_metadata_file_get_number_of_file_entries(
	          NULL,
	          &number_of_file_entries,
	          &error );

	FSNTFS_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	FSNTFS_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	if( number_of_file_entries_is_set != 0 )
	{
		result = libfsntfs_mft_metadata_file_get_number_of_file_entries(
		          mft_metadata_file,
		          NULL,
		          &error );

		FSNTFS_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 -1 );

		FSNTFS_TEST_ASSERT_IS_NOT_NULL(
		 "error",
		 error );

		libcerror_error_free(
		 &error );
	}
	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	return( 0 );
}

/* The main program
 */
#if defined( HAVE_WIDE_SYSTEM_CHARACTER )
int wmain(
     int argc,
     wchar_t * const argv[] )
#else
int main(
     int argc,
     char * const argv[] )
#endif
{
	libbfio_handle_t *file_io_handle                 = NULL;
	libcerror_error_t *error                         = NULL;
	libfsntfs_mft_metadata_file_t *mft_metadata_file = NULL;
	system_character_t *option_offset                = NULL;
	system_character_t *source                       = NULL;
	system_integer_t option                          = 0;
	size_t string_length                             = 0;
	off64_t mft_metadata_file_offset                 = 0;
	int result                                       = 0;

	while( ( option = fsntfs_test_getopt(
	                   argc,
	                   argv,
	                   _SYSTEM_STRING( "o:" ) ) ) != (system_integer_t) -1 )
	{
		switch( option )
		{
			case (system_integer_t) '?':
			default:
				fprintf(
				 stderr,
				 "Invalid argument: %" PRIs_SYSTEM ".\n",
				 argv[ optind - 1 ] );

				return( EXIT_FAILURE );

			case (system_integer_t) 'o':
				option_offset = optarg;

				break;
		}
	}
	if( optind < argc )
	{
		source = argv[ optind ];
	}
	if( option_offset != NULL )
	{
		string_length = system_string_length(
		                 option_offset );

		result = fsntfs_test_system_string_copy_from_64_bit_in_decimal(
		          option_offset,
		          string_length + 1,
		          (uint64_t *) &mft_metadata_file_offset,
		          &error );

		FSNTFS_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 1 );

	        FSNTFS_TEST_ASSERT_IS_NULL(
	         "error",
	         error );
	}
#if defined( HAVE_DEBUG_OUTPUT ) && defined( FSNTFS_TEST_MFT_METADATA_FILE_VERBOSE )
	libfsntfs_notify_set_verbose(
	 1 );
	libfsntfs_notify_set_stream(
	 stderr,
	 NULL );
#endif

	FSNTFS_TEST_RUN(
	 "libfsntfs_mft_metadata_file_initialize",
	 fsntfs_test_mft_metadata_file_initialize );

	FSNTFS_TEST_RUN(
	 "libfsntfs_mft_metadata_file_free",
	 fsntfs_test_mft_metadata_file_free );

#if !defined( __BORLANDC__ ) || ( __BORLANDC__ >= 0x0560 )
	if( source != NULL )
	{
		result = libbfio_file_range_initialize(
		          &file_io_handle,
		          &error );

		FSNTFS_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 1 );

	        FSNTFS_TEST_ASSERT_IS_NOT_NULL(
	         "file_io_handle",
	         file_io_handle );

	        FSNTFS_TEST_ASSERT_IS_NULL(
	         "error",
	         error );

		string_length = system_string_length(
		                 source );

#if defined( HAVE_WIDE_SYSTEM_CHARACTER )
		result = libbfio_file_range_set_name_wide(
		          file_io_handle,
		          source,
		          string_length,
		          &error );
#else
		result = libbfio_file_range_set_name(
		          file_io_handle,
		          source,
		          string_length,
		          &error );
#endif
		FSNTFS_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 1 );

	        FSNTFS_TEST_ASSERT_IS_NULL(
	         "error",
	         error );

		result = libbfio_file_range_set(
		          file_io_handle,
		          mft_metadata_file_offset,
		          0,
		          &error );

		FSNTFS_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 1 );

	        FSNTFS_TEST_ASSERT_IS_NULL(
	         "error",
	         error );

		result = libfsntfs_check_mft_metadata_file_signature_file_io_handle(
		          file_io_handle,
		          &error );

		FSNTFS_TEST_ASSERT_NOT_EQUAL_INT(
		 "result",
		 result,
		 -1 );

		FSNTFS_TEST_ASSERT_IS_NULL(
		 "error",
		 error );
	}
	if( ( result != 0 )
	 && ( mft_metadata_file_offset == 0 ) )
	{
		FSNTFS_TEST_RUN_WITH_ARGS(
		 "libfsntfs_mft_metadata_file_open",
		 fsntfs_test_mft_metadata_file_open,
		 source );

#if defined( HAVE_WIDE_CHARACTER_TYPE )

		FSNTFS_TEST_RUN_WITH_ARGS(
		 "libfsntfs_mft_metadata_file_open_wide",
		 fsntfs_test_mft_metadata_file_open_wide,
		 source );

#endif /* defined( HAVE_WIDE_CHARACTER_TYPE ) */

#if defined( LIBFSNTFS_HAVE_BFIO )

		/* TODO add test for libfsntfs_mft_metadata_file_open_file_io_handle */

#endif /* defined( LIBFSNTFS_HAVE_BFIO ) */

		FSNTFS_TEST_RUN(
		 "libfsntfs_mft_metadata_file_close",
		 fsntfs_test_mft_metadata_file_close );

		FSNTFS_TEST_RUN_WITH_ARGS(
		 "libfsntfs_mft_metadata_file_open_close",
		 fsntfs_test_mft_metadata_file_open_close,
		 source );
	}
	if( result != 0 )
	{
		/* Initialize test
		 */
		result = fsntfs_test_mft_metadata_file_open_source(
		          &mft_metadata_file,
		          file_io_handle,
		          &error );

		FSNTFS_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 1 );

		FSNTFS_TEST_ASSERT_IS_NOT_NULL(
		 "mft_metadata_file",
		 mft_metadata_file );

		FSNTFS_TEST_ASSERT_IS_NULL(
		 "error",
		 error );

		FSNTFS_TEST_RUN_WITH_ARGS(
		 "libfsntfs_mft_metadata_file_signal_abort",
		 fsntfs_test_mft_metadata_file_signal_abort,
		 mft_metadata_file );

#if defined( __GNUC__ ) && !defined( LIBFSNTFS_DLL_IMPORT )

		/* TODO: add tests for libfsntfs_mft_metadata_file_open_read */

#endif /* defined( __GNUC__ ) && !defined( LIBFSNTFS_DLL_IMPORT ) */

		FSNTFS_TEST_RUN_WITH_ARGS(
		 "libfsntfs_mft_metadata_file_get_utf8_volume_name_size",
		 fsntfs_test_mft_metadata_file_get_utf8_volume_name_size,
		 mft_metadata_file );

		FSNTFS_TEST_RUN_WITH_ARGS(
		 "libfsntfs_mft_metadata_file_get_utf8_volume_name",
		 fsntfs_test_mft_metadata_file_get_utf8_volume_name,
		 mft_metadata_file );

		FSNTFS_TEST_RUN_WITH_ARGS(
		 "libfsntfs_mft_metadata_file_get_utf16_volume_name_size",
		 fsntfs_test_mft_metadata_file_get_utf16_volume_name_size,
		 mft_metadata_file );

		FSNTFS_TEST_RUN_WITH_ARGS(
		 "libfsntfs_mft_metadata_file_get_utf16_volume_name",
		 fsntfs_test_mft_metadata_file_get_utf16_volume_name,
		 mft_metadata_file );

		/* TODO: add tests for libfsntfs_mft_metadata_file_get_volume_version */

		FSNTFS_TEST_RUN_WITH_ARGS(
		 "libfsntfs_mft_metadata_file_get_number_of_file_entries",
		 fsntfs_test_mft_metadata_file_get_number_of_file_entries,
		 mft_metadata_file );

		/* TODO: add tests for libfsntfs_mft_metadata_file_get_file_entry_by_index */

		/* Clean up
		 */
		result = fsntfs_test_mft_metadata_file_close_source(
		          &mft_metadata_file,
		          &error );

		FSNTFS_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 0 );

		FSNTFS_TEST_ASSERT_IS_NULL(
		 "mft_metadata_file",
		 mft_metadata_file );

		FSNTFS_TEST_ASSERT_IS_NULL(
		 "error",
		 error );
	}
	if( file_io_handle != NULL )
	{
		result = libbfio_handle_free(
		          &file_io_handle,
		          &error );

		FSNTFS_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 1 );

		FSNTFS_TEST_ASSERT_IS_NULL(
	         "file_io_handle",
	         file_io_handle );

	        FSNTFS_TEST_ASSERT_IS_NULL(
	         "error",
	         error );
	}
#endif /* !defined( __BORLANDC__ ) || ( __BORLANDC__ >= 0x0560 ) */

	return( EXIT_SUCCESS );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	if( mft_metadata_file != NULL )
	{
		fsntfs_test_mft_metadata_file_close_source(
		 &mft_metadata_file,
		 NULL );
	}
	if( file_io_handle != NULL )
	{
		libbfio_handle_free(
		 &file_io_handle,
		 NULL );
	}
	return( EXIT_FAILURE );
}

