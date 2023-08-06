
####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was wolfram_modelConfig.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

####################################################################################

include(CMakeFindDependencyMacro)

#### Required dependencies  ####
# find_dependency(Boost REQUIRED COMPONENTS program_options filesystem graph)

#### Optional dependencies based on wolfram_model options ####
# if() #if(${SG_REQUIRES_ITK})
#   find_dependency(ITK REQUIRED COMPONENTS
#     
#     CONFIG)
# endif()

get_filename_component(WOLFRAM_MODEL_CMAKE_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)
if(NOT TARGET SetReplace)
  include ("${WOLFRAM_MODEL_CMAKE_DIR}/wolfram_modelTargets.cmake")
endif()
