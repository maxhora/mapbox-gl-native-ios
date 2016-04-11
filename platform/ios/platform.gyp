{
  'variables': {
    'loop_lib': 'darwin',
    'headless_lib': 'eagl',
  },
  'xcode_settings': {
     # Force all build output to the build directory. Must
     # be an absolute path or xcodebuild will ignore it.
    'SYMROOT': '<!(cd ../../build/ios-all && pwd)',
  },
  'includes': [
    '../../mbgl.gypi',
    '../../test/test.gypi',
  ],
  'target_defaults': {
    'target_conditions': [
      ['_type == "static_library"', {
        'xcode_settings': {
          'SDKROOT': 'iphoneos',
          'SUPPORTED_PLATFORMS': 'iphonesimulator iphoneos',
          'IPHONEOS_DEPLOYMENT_TARGET': '7.0',
          'TARGETED_DEVICE_FAMILY': '1,2',
          'GCC_VERSION': 'com.apple.compilers.llvm.clang.1_0',
          'CODE_SIGN_IDENTITY': 'iPhone Developer',
        },
        'configurations': {
          'Release': {
            'xcode_settings': {
              'ARCHS': [ "armv7", "armv7s", "arm64", "i386", "x86_64" ],
            },
          },
        },
      }],
    ],
  },
  'targets': [
    {
      'target_name': 'test',
      'type': 'executable',
      'product_name': 'ios-test',
      'product_extension': 'app',
      'mac_bundle': 1,

      'dependencies': [
        'test-lib',
        'platform-lib',
      ],

      'sources': [
        '../../test/src/main.mm',
#        '../../src/mbgl/util/premultiply.cpp',
      ],

      'xcode_settings': {
        'SDKROOT': 'iphoneos',
        'SUPPORTED_PLATFORMS': 'iphonesimulator iphoneos',
        'INFOPLIST_FILE': '../../test/src/app-info.plist',
        'IPHONEOS_DEPLOYMENT_TARGET': '8.0',
        'TARGETED_DEVICE_FAMILY': '1,2',
        'COPY_PHASE_STRIP': 'NO',
        'CLANG_ENABLE_OBJC_ARC': 'YES',
        'CLANG_ENABLE_MODULES': 'YES',
        'CODE_SIGN_IDENTITY': 'iPhone Developer',
      },

      'copies': [{
        'destination': '<(PRODUCT_DIR)/$(WRAPPER_NAME)/test',
        'files': [ '../../test/fixtures' ],
      }],

      'link_settings': {
        'libraries': [
          '$(SDKROOT)/System/Library/Frameworks/CoreGraphics.framework',
          '$(SDKROOT)/System/Library/Frameworks/GLKit.framework',
          '$(SDKROOT)/System/Library/Frameworks/ImageIO.framework',
          '$(SDKROOT)/System/Library/Frameworks/MobileCoreServices.framework',
          '$(SDKROOT)/System/Library/Frameworks/OpenGLES.framework',
        ],
      },
    },
    {
      'target_name': 'platform-lib',
      'product_name': 'mbgl-platform-ios',
      'type': 'static_library',
      'standalone_static_library': 1,
      'hard_dependency': 1,
      'dependencies': [
        'core',
      ],

      'include_dirs': [
        'include',
        '../darwin/include',
        '../default',
        '../../include',
        '../../src', # TODO: eliminate
      ],

      'sources': [
        '../default/asset_file_source.cpp',
        '../default/default_file_source.cpp',
        '../default/online_file_source.cpp',
        '../default/mbgl/storage/offline.hpp',
        '../default/mbgl/storage/offline.cpp',
        '../default/mbgl/storage/offline_database.hpp',
        '../default/mbgl/storage/offline_database.cpp',
        '../default/mbgl/storage/offline_download.hpp',
        '../default/mbgl/storage/offline_download.cpp',
        '../default/sqlite3.hpp',
        '../default/sqlite3.cpp',
        '../darwin/src/http_file_source.mm',
        '../darwin/src/log_nslog.mm',
        '../darwin/src/string_nsstring.mm',
        '../darwin/src/image.mm',
        '../darwin/src/nsthread.mm',
        '../darwin/src/reachability.m',
      ],

      'variables': {
        'cflags_cc': [
          '<@(boost_cflags)',
          '<@(sqlite_cflags)',
          '<@(zlib_cflags)',
          '<@(rapidjson_cflags)',
          '<@(variant_cflags)',
        ],
        'ldflags': [
          '<@(sqlite_ldflags)',
          '<@(zlib_ldflags)',
        ],
        'libraries': [
          '<@(sqlite_static_libs)',
          '<@(zlib_static_libs)',
        ],
      },

      'xcode_settings': {
        'OTHER_CPLUSPLUSFLAGS': [ '<@(cflags_cc)' ],
        'CLANG_ENABLE_OBJC_ARC': 'YES',
        'CLANG_ENABLE_MODULES': 'YES',
      },

      'link_settings': {
        'libraries': [ '<@(libraries)' ],
        'xcode_settings': {
          'OTHER_LDFLAGS': [ '<@(ldflags)' ],
        },
      },
    },
  ],
}
