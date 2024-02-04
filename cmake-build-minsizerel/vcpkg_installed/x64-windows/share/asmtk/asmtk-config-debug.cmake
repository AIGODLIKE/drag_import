#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "asmjit::asmtk" for configuration "Debug"
set_property(TARGET asmjit::asmtk APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(asmjit::asmtk PROPERTIES
  IMPORTED_IMPLIB_DEBUG "${_IMPORT_PREFIX}/debug/lib/asmtk.lib"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/debug/bin/asmtk.dll"
  )

list(APPEND _cmake_import_check_targets asmjit::asmtk )
list(APPEND _cmake_import_check_files_for_asmjit::asmtk "${_IMPORT_PREFIX}/debug/lib/asmtk.lib" "${_IMPORT_PREFIX}/debug/bin/asmtk.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
