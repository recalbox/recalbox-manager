/**
* Grunt config with watch, cssmin and uglify tasks
* 
* Depend on asset manifest in project_dir to know assets to manage.
*/
module.exports = function(grunt) {
    var path = require('path'),
        project_dir = 'project',
        static_dir = path.join(project_dir, 'webapp_statics'),
        asset_manifest = grunt.file.readJSON(path.join(project_dir, 'assets.json')),
        // Prepend all map entries (key and values) with a path
        prepend_dir_on_paths = function(dir, file_map) {
            var prepended_map = {};
            // Go through all the map entries
            for(var keyname in file_map){
                // New key prepended with the map
                var distkey = path.join(dir, keyname);
                // Init the futur item list
                prepended_map[distkey] = [];
                // Prepend list items
                for (var i=0; i<file_map[keyname].length ;i++){
                    prepended_map[distkey].push( path.join(dir, file_map[keyname][i]) );
                }
            }
            return prepended_map;
        };
    
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        
        watch: {
            cssmin: {
                files: [path.join(static_dir, 'css/*.css')],
                tasks:  ['cssmin'],
                options: {
                    spawn: false, // for grunt-contrib-watch v0.5.0+, "nospawn: true" for lower versions. Without this option specified express won't be reloaded
                    livereload: true
                }
            }
        },

        cssmin: {
            target: {
                options: {
                    banner: '/* Recalbox minified CSS. Minified on <%= grunt.template.today("yyyy-mm-dd hh:MM:ss")%> by GruntJS-cssmin */'
                },
                files: prepend_dir_on_paths(static_dir, asset_manifest.stylesheets)
            }
        },
        uglify: {
            options: {
                mangle: false // prevent changes to variable name. Maybe set to 'true' after testing ?
            },
            target: {
                files: prepend_dir_on_paths(static_dir, asset_manifest.javascripts)
            }
        }
    });

    // Load plugins
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-uglify');

    // Create custom tasks
    grunt.registerTask('server', [ 'watch' ]);
};
