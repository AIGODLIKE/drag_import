#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Zycore::Zycore" for configuration "Debug"
set_property(TARGET Zycore::Zycore APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(Zycore::Zycore PROPERTIES
  IMPORTED_IMPLIB_DEBUG "${_IMPORT_PREFIX}/debug/lib/Zycore.lib"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/debug/bin/Zycore.dll"
  )

list(APPEND _cmake_import_check_targets Zycore::Zycore )
list(APPEND _cmake_import_check_files_for_Zycore::Zycore "${_IMPORT_PREFIX}/debug/lib/Zycore.lib" "${_IMPORT_PREFIX}/debug/bin/Zycore.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
