/*global module:false*/
module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    lint: {
      files: ['js/*.js', 'test/*/*.js']
    },
    watch: {
      files: [
        '<config:lint.files>',
        'coffee/*.coffee'
      ],
      tasks: [
        'coffee',
        'lint',
        'jasmine'
      ]
    },
    coffee: {
      app: {
        src: ['coffee/*.coffee'],
        dest: 'js/',
        options: {
            bare: false
        }
      }
    },
    'closure-compiler': {
      frontend: {
        closurePath: '../../closure-compiler',
        js: 'js/*.js',
        jsOutputFile: 'build/js/scripts.min.js',
        options: {
          compilation_level: 'SIMPLE_OPTIMIZATIONS',
          language_in: 'ECMASCRIPT5_STRICT'
        }
      }
    },
    jasmine: {
      all: ['tests/specrunner.html']
    },
    jshint: {
      options: {
        curly: true,
        eqeqeq: true,
        immed: true,
        latedef: true,
        newcap: true,
        noarg: true,
        sub: true,
        undef: true,
        boss: true,
        eqnull: true,
        browser: true
      },
      globals: {
        $: true
      }
    }
  });

  // Default task.
  grunt.registerTask('default', 'coffee closure-compiler');
  grunt.loadNpmTasks('grunt-coffee');
  grunt.loadNpmTasks('grunt-jasmine-task');
  grunt.loadNpmTasks('grunt-closure-compiler');
};