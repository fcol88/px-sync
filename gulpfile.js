const gulp = require('gulp');
const sass = require('gulp-sass');
const del = require('del');

gulp.task('styles', () => {
	return nhs = gulp.src('px_sync/static/scss/style.scss').
		pipe(sass().on('error', sass.logError))
		.pipe(gulp.dest('px_sync/static/css/'));
});

gulp.task('clean', () => {
	return del([
		'px_sync/static/css/style.css',
	]);
})

gulp.task('default', gulp.series(['clean', 'styles']));
