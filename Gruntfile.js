module.exports = function (grunt) {
    'use strict';
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        less: {
            dist: {
                options: {
                    paths: [],
                    strictMath: false,
                    sourceMap: true,
                    outputSourceFiles: true,
                    sourceMapURL: '++resource++bda.plone.discount.css.map',
                    sourceMapFilename: 'src/bda/plone/discount/browser/discount.css.map',
                    modifyVars: {
                        "isPlone": "false"
                    }
                },
                files: {
                    'src/bda/plone/discount/browser/discount.css': 'src/bda/plone/discount/browser/discount.less',
                }
            }
        },
        sed: {
            sed0: {
                path: 'src/bda/plone/discount/browser/discount.css.map',
                pattern: 'src/bda/plone/discount/browser/discount.less',
                replacement: '++resource++bda.plone.discount.less',
            }
        },
        watch: {
            scripts: {
                files: ['src/bda/plone/discount/browser/discount.less'],
                tasks: ['less', 'sed']
            }
        }
    });
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-sed');
    grunt.registerTask('default', ['watch']);
    grunt.registerTask('compile', ['less', 'sed']);
};
