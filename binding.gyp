{
  'includes': [ 'common.gypi' ],
  'variables': {
      'runtime_link%':'shared',
  },
  'conditions': [
      ['OS=="win"', {
        'variables': {
          'PROTOBUF_INCLUDES%':'C:/dev2/protobuf/vsprojects/include',
          'PROTOBUF_LIBS%':'C:/dev2/protobuf/vsprojects/Release',
          'PROTOBUF_LIBRARY%':'libprotobuf-lite.lib',
        }
      }]
  ],
  'targets': [
    {
      'target_name': '_mapnik',
      'sources': [
          "src/node_mapnik.cpp",
          "src/mapnik_map.cpp",
          "src/mapnik_color.cpp",
          "src/mapnik_geometry.cpp",
          "src/mapnik_feature.cpp",
          "src/mapnik_image.cpp",
          "src/mapnik_image_view.cpp",
          "src/mapnik_grid.cpp",
          "src/mapnik_grid_view.cpp",
          "src/mapnik_js_datasource.cpp",
          "src/mapnik_memory_datasource.cpp",
          "src/mapnik_palette.cpp",
          "src/mapnik_projection.cpp",
          "src/mapnik_proj_transform.cpp",
          "src/mapnik_layer.cpp",
          "src/mapnik_datasource.cpp",
          "src/mapnik_featureset.cpp",
          "src/mapnik_expression.cpp",
          "src/mapnik_query.cpp",
          "src/mapnik_cairo_surface.cpp",
          "src/mapnik_vector_tile.cpp",
          "node_modules/mapnik-vector-tile/src/vector_tile.pb.cc"
      ],
      'include_dirs': [
          './node_modules/mapnik-vector-tile/src/',
          './src'
      ],
      'conditions': [
        ['OS=="win"', {
            'include_dirs':[
                '<!@(mapnik-config --includes)',
                '<!@(mapnik-config --dep-includes)',
                '<@(PROTOBUF_INCLUDES)'
              ],
            'defines': ['<!@(mapnik-config --defines)'],
            'libraries': [
                '<!@(mapnik-config --libs)',
                '<!@(mapnik-config --dep-libs)',
                '<@(PROTOBUF_LIBRARY)'
            ],
            'msvs_disabled_warnings': [ 4244,4005,4506,4345,4804 ],
            'msvs_settings': {
            'VCCLCompilerTool': {
                # note: not respected, need to change in C:\Users\mapnik\.node-gyp\*\common.gypi
                'ExceptionHandling': 1,
                'RuntimeTypeInfo':'true',
                'RuntimeLibrary': '2'  # /MD http://stackoverflow.com/questions/757418/should-i-compile-with-md-or-mt
            },
            'VCLinkerTool': {
                'AdditionalOptions': [
                    # https://github.com/mapnik/node-mapnik/issues/74
                    '/FORCE:MULTIPLE'
                ],
                'AdditionalLibraryDirectories': [
                    '<!@(mapnik-config --ldflags)',
                    '<@(PROTOBUF_LIBS)'
                ],
            },
          }
        },{
            'cflags_cc!': ['-fno-rtti', '-fno-exceptions'],
            'cflags_cc' : [
                '<!@(mapnik-config --cflags)',
                '<!@(pkg-config protobuf --cflags)'
            ],
            'libraries':[
                '<!@(mapnik-config --libs)',
                '<!@(pkg-config protobuf --libs-only-L)',
                '-lprotobuf-lite'
            ],
            'conditions': [
              ['runtime_link == "static"', {
                  'libraries': [
                    '<!@(mapnik-config --ldflags)',
                    '<!@(mapnik-config --dep-libs)'
                   ]
              }]
            ],
        }]
      ],
      # this has to be per target to correctly
      # override node-gyp defaults
      'xcode_settings': {
          'OTHER_CPLUSPLUSFLAGS':[
              '<!@(mapnik-config --cflags)',
              '<!@(pkg-config protobuf --cflags)'
          ],
          'GCC_ENABLE_CPP_RTTI': 'YES',
          'GCC_ENABLE_CPP_EXCEPTIONS': 'YES',
          'CLANG_CXX_LANGUAGE_STANDARD':'c++11',
          'MACOSX_DEPLOYMENT_TARGET':'10.7'
      },
      'msvs_settings': {
          'VCCLCompilerTool': {
              'ExceptionHandling': 1,
              'RuntimeTypeInfo':'true',
              'RuntimeLibrary': '3'  # /MDd
          }
      }
    },
    {
      'target_name': 'action_after_build',
      'type': 'none',
      'dependencies': [ '_mapnik' ],
      'actions': [
          {
            'action_name': 'generate_setting',
            'inputs': [
              'gen_settings.py'
            ],
            'outputs': [
              'lib/mapnik_settings.js'
            ],
            'action': ['python', 'gen_settings.py']
          },
      ],
      'copies': [
          {
            'files': [ '<(PRODUCT_DIR)/_mapnik.node' ],
            'destination': './lib/'
          }
      ]
    }
  ]
}