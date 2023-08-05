#!/bin/bash
# Tests library functions and types.
#
# Version: 20190216

EXIT_SUCCESS=0;
EXIT_FAILURE=1;
EXIT_IGNORE=77;

LIBRARY_TESTS="attribute attribute_list_entry bitmap_values buffer_data_handle cluster_block cluster_block_data cluster_block_stream cluster_block_vector compressed_block compressed_block_data_handle compressed_block_vector compressed_data_handle compression compression_unit_data_handle compression_unit_descriptor data_extent data_run data_stream directory_entries_tree directory_entry error file_entry file_name_attribute file_name_values file_system fixup_values index index_entry index_entry_header index_entry_vector index_node index_node_header index_root_header index_value io_handle logged_utility_stream_values mft mft_attribute mft_attribute_list mft_attribute_list_entry mft_entry mft_entry_header name notify object_identifier_values path_hint profiler reparse_point_attribute reparse_point_values sds_index_value security_descriptor_index security_descriptor_index_value security_descriptor_values standard_information_values txf_data_values usn_change_journal volume_header volume_information_attribute volume_information_values volume_name_attribute volume_name_values";
LIBRARY_TESTS_WITH_INPUT="mft_metadata_file support volume";
OPTION_SETS="offset";

INPUT_GLOB="*";

run_test()
{
	local TEST_NAME=$1;

	local TEST_DESCRIPTION="Testing: ${TEST_NAME}";
	local TEST_EXECUTABLE="./fsntfs_test_${TEST_NAME}";

	if ! test -x "${TEST_EXECUTABLE}";
	then
		TEST_EXECUTABLE="${TEST_EXECUTABLE}.exe";
	fi

	# TODO: add support for TEST_PROFILE and OPTION_SETS?
	run_test_with_arguments "${TEST_DESCRIPTION}" "${TEST_EXECUTABLE}";
	local RESULT=$?;

	return ${RESULT};
}

run_test_with_input()
{
	local TEST_NAME=$1;

	local TEST_DESCRIPTION="Testing: ${TEST_NAME}";
	local TEST_EXECUTABLE="./fsntfs_test_${TEST_NAME}";

	if ! test -x "${TEST_EXECUTABLE}";
	then
		TEST_EXECUTABLE="${TEST_EXECUTABLE}.exe";
	fi

	if ! test -d "input";
	then
		echo "Test input directory not found.";

		return ${EXIT_IGNORE};
	fi
	local RESULT=`ls input/* | tr ' ' '\n' | wc -l`;

	if test ${RESULT} -eq ${EXIT_SUCCESS};
	then
		echo "No files or directories found in the test input directory";

		return ${EXIT_IGNORE};
	fi

	local TEST_PROFILE_DIRECTORY=$(get_test_profile_directory "input" "libfsntfs");

	local IGNORE_LIST=$(read_ignore_list "${TEST_PROFILE_DIRECTORY}");

	RESULT=${EXIT_SUCCESS};

	for TEST_SET_INPUT_DIRECTORY in input/*;
	do
		if ! test -d "${TEST_SET_INPUT_DIRECTORY}";
		then
			continue;
		fi
		if check_for_directory_in_ignore_list "${TEST_SET_INPUT_DIRECTORY}" "${IGNORE_LIST}";
		then
			continue;
		fi

		local TEST_SET_DIRECTORY=$(get_test_set_directory "${TEST_PROFILE_DIRECTORY}" "${TEST_SET_INPUT_DIRECTORY}");

		local OLDIFS=${IFS};

		# IFS="\n" is not supported by all platforms.
		IFS="
";

		if test -f "${TEST_SET_DIRECTORY}/files";
		then
			for INPUT_FILE in `cat ${TEST_SET_DIRECTORY}/files | sed "s?^?${TEST_SET_INPUT_DIRECTORY}/?"`;
			do
				if test "${OSTYPE}" = "msys";
				then
					# A test executable built with MinGW expects a Windows path.
					INPUT_FILE=`echo ${INPUT_FILE} | sed 's?/?\\\\?g'`;
				fi
				run_test_on_input_file_with_options "${TEST_SET_DIRECTORY}" "${TEST_DESCRIPTION}" "default" "${OPTION_SETS}" "${TEST_EXECUTABLE}" "${INPUT_FILE}";
				RESULT=$?;

				if test ${RESULT} -ne ${EXIT_SUCCESS};
				then
					break;
				fi
			done
		else
			for INPUT_FILE in `ls -1d ${TEST_SET_INPUT_DIRECTORY}/${INPUT_GLOB}`;
			do
				if test "${OSTYPE}" = "msys";
				then
					# A test executable built with MinGW expects a Windows path.
					INPUT_FILE=`echo ${INPUT_FILE} | sed 's?/?\\\\?g'`;
				fi
				run_test_on_input_file_with_options "${TEST_SET_DIRECTORY}" "${TEST_DESCRIPTION}" "default" "${OPTION_SETS}" "${TEST_EXECUTABLE}" "${INPUT_FILE}";
				RESULT=$?;

				if test ${RESULT} -ne ${EXIT_SUCCESS};
				then
					break;
				fi
			done
		fi
		IFS=${OLDIFS};

		if test ${RESULT} -ne ${EXIT_SUCCESS};
		then
			break;
		fi
	done

	return ${RESULT};
}

if ! test -z ${SKIP_LIBRARY_TESTS};
then
	exit ${EXIT_IGNORE};
fi

TEST_RUNNER="tests/test_runner.sh";

if ! test -f "${TEST_RUNNER}";
then
	TEST_RUNNER="./test_runner.sh";
fi

if ! test -f "${TEST_RUNNER}";
then
	echo "Missing test runner: ${TEST_RUNNER}";

	exit ${EXIT_FAILURE};
fi

source ${TEST_RUNNER};

RESULT=${EXIT_IGNORE};

for TEST_NAME in ${LIBRARY_TESTS};
do
	run_test "${TEST_NAME}";
	RESULT=$?;

	if test ${RESULT} -ne ${EXIT_SUCCESS};
	then
		break;
	fi
done

if test ${RESULT} -ne ${EXIT_SUCCESS} && test ${RESULT} -ne ${EXIT_IGNORE};
then
	exit ${RESULT};
fi

for TEST_NAME in ${LIBRARY_TESTS_WITH_INPUT};
do
	if test -d "input";
	then
		run_test_with_input "${TEST_NAME}";
		RESULT=$?;
	else
		run_test "${TEST_NAME}";
		RESULT=$?;
	fi

	if test ${RESULT} -ne ${EXIT_SUCCESS};
	then
		break;
	fi
done

exit ${RESULT};

