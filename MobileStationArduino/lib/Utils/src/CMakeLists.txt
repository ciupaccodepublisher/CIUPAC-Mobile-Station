message("--------- Processing Utils cmakes")

add_library(Utils INTERFACE)
target_sources(Utils INTERFACE AknControl.cpp)
