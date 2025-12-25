cmake_minimum_required(VERSION 3.10)
project(cogman_kernel VERSION 2.0.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include directories
include_directories(include)

# Source files
set(KERNEL_SOURCES
    src/core_formulas.cpp
    src/energy_projection.cpp
    src/gate_core.cpp
    src/core9_gate.cpp
    src/gate_policy.cpp
    src/kernel_api.cpp
    src/errors.cpp
    src/eps8.cpp
    src/utils.cpp
)

# Create library (shared for Python bindings)
add_library(cogman_kernel SHARED ${KERNEL_SOURCES})

# Also create static library
add_library(cogman_kernel_static STATIC ${KERNEL_SOURCES})
set_target_properties(cogman_kernel_static PROPERTIES OUTPUT_NAME cogman_kernel)

# Install targets
install(TARGETS cogman_kernel
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib
)

install(DIRECTORY include/cogman_kernel
    DESTINATION include
    FILES_MATCHING PATTERN "*.hpp"
)

# Tests
add_executable(test_core_formulas tests/test_core_formulas.cpp)
target_link_libraries(test_core_formulas cogman_kernel)

add_executable(test_energy_bounds tests/test_energy_bounds.cpp)
target_link_libraries(test_energy_bounds cogman_kernel)

add_executable(test_determinism tests/test_determinism.cpp)
target_link_libraries(test_determinism cogman_kernel)

add_executable(test_input_validation tests/test_input_validation.cpp)
target_link_libraries(test_input_validation cogman_kernel)

# Examples
add_executable(example_basic examples/example_basic.cpp)
target_link_libraries(example_basic cogman_kernel)

add_executable(example_decision_gate examples/example_decision_gate.cpp)
target_link_libraries(example_decision_gate cogman_kernel)

add_executable(example_core9 examples/example_core9.cpp)
target_link_libraries(example_core9 cogman_kernel)

add_executable(example_policy_loader examples/example_policy_loader.cpp)
target_link_libraries(example_policy_loader cogman_kernel)

add_executable(example_error_handling examples/example_error_handling.cpp)
target_link_libraries(example_error_handling cogman_kernel)
