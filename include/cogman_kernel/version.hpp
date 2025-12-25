/**
 * Cogman Kernel - Version Information
 * 
 * Version: v2.0-LOCKED
 */

#ifndef COGMAN_KERNEL_VERSION_HPP
#define COGMAN_KERNEL_VERSION_HPP

#define COGMAN_KERNEL_VERSION_MAJOR 2
#define COGMAN_KERNEL_VERSION_MINOR 0
#define COGMAN_KERNEL_VERSION_PATCH 0
#define COGMAN_KERNEL_VERSION_STRING "2.0.0"

namespace cogman_kernel {

struct Version {
    static constexpr int major = COGMAN_KERNEL_VERSION_MAJOR;
    static constexpr int minor = COGMAN_KERNEL_VERSION_MINOR;
    static constexpr int patch = COGMAN_KERNEL_VERSION_PATCH;
    static constexpr const char* string = COGMAN_KERNEL_VERSION_STRING;
};

} // namespace cogman_kernel

#endif // COGMAN_KERNEL_VERSION_HPP

