#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "wolfram_model::SetReplace" for configuration "Release"
set_property(TARGET wolfram_model::SetReplace APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(wolfram_model::SetReplace PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libSetReplace.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS wolfram_model::SetReplace )
list(APPEND _IMPORT_CHECK_FILES_FOR_wolfram_model::SetReplace "${_IMPORT_PREFIX}/lib64/libSetReplace.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
