# CMake generated Testfile for 
# Source directory: /Users/julienenoch/ATO-code/eclipse-zenoh-ato-fork/apis/zenoh-python/zenoh-c
# Build directory: /Users/julienenoch/ATO-code/eclipse-zenoh-ato-fork/apis/zenoh-python/zenoh-c/build
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(z_data_struct "z_data_struct")
set_tests_properties(z_data_struct PROPERTIES  _BACKTRACE_TRIPLES "/Users/julienenoch/ATO-code/eclipse-zenoh-ato-fork/apis/zenoh-python/zenoh-c/CMakeLists.txt;190;add_test;/Users/julienenoch/ATO-code/eclipse-zenoh-ato-fork/apis/zenoh-python/zenoh-c/CMakeLists.txt;0;")
add_test(z_mvar_test "z_mvar_test")
set_tests_properties(z_mvar_test PROPERTIES  _BACKTRACE_TRIPLES "/Users/julienenoch/ATO-code/eclipse-zenoh-ato-fork/apis/zenoh-python/zenoh-c/CMakeLists.txt;191;add_test;/Users/julienenoch/ATO-code/eclipse-zenoh-ato-fork/apis/zenoh-python/zenoh-c/CMakeLists.txt;0;")
add_test(z_rname_test "z_rname_test")
set_tests_properties(z_rname_test PROPERTIES  _BACKTRACE_TRIPLES "/Users/julienenoch/ATO-code/eclipse-zenoh-ato-fork/apis/zenoh-python/zenoh-c/CMakeLists.txt;192;add_test;/Users/julienenoch/ATO-code/eclipse-zenoh-ato-fork/apis/zenoh-python/zenoh-c/CMakeLists.txt;0;")
add_test(zn_client_test "bash" "routed.sh" "zn_client_test")
set_tests_properties(zn_client_test PROPERTIES  _BACKTRACE_TRIPLES "/Users/julienenoch/ATO-code/eclipse-zenoh-ato-fork/apis/zenoh-python/zenoh-c/CMakeLists.txt;193;add_test;/Users/julienenoch/ATO-code/eclipse-zenoh-ato-fork/apis/zenoh-python/zenoh-c/CMakeLists.txt;0;")
add_test(zn_large_data_test "bash" "routed.sh" "zn_large_data_test")
set_tests_properties(zn_large_data_test PROPERTIES  _BACKTRACE_TRIPLES "/Users/julienenoch/ATO-code/eclipse-zenoh-ato-fork/apis/zenoh-python/zenoh-c/CMakeLists.txt;194;add_test;/Users/julienenoch/ATO-code/eclipse-zenoh-ato-fork/apis/zenoh-python/zenoh-c/CMakeLists.txt;0;")
