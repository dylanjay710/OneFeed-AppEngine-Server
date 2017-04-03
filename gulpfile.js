var gulp = require('gulp'),
    browserSync = require("browser-sync"),
    reload = browserSync.reload;

var files = {
    main: "main.py",
};

gulp.task("default", function() {
    console.log("default task running")
});

gulp.task("serve:dev", function() {

	browserSync.init({
    	proxy: "localhost:8080"
    });

    gulp.watch(files.main).on('change', reload);

    

});