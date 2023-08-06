define("jupyter_vtk", [], function() { return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/index.ts");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/*! exports provided: name, version, description, keywords, files, homepage, bugs, license, author, main, repository, scripts, dependencies, devDependencies, jupyterlab, default */
/***/ (function(module) {

module.exports = JSON.parse("{\"name\":\"jupyter_vtk\",\"version\":\"0.1.0\",\"description\":\"VTK visualisation for jupyter lab\",\"keywords\":[\"jupyter\",\"jupyterlab\",\"jupyterlab-extension\",\"widgets\"],\"files\":[\"dist/*.js\",\"dist/*.woff\",\"dist/*.svg\",\"dist/*.eot\",\"dist/*.ttf\",\"css/*.css\",\"dist/itk/**\"],\"homepage\":\"https://github.com//jupyter_vtk\",\"bugs\":{\"url\":\"https://github.com//jupyter_vtk/issues\"},\"license\":\"BSD-3-Clause\",\"author\":{\"name\":\"Trung Le\",\"email\":\"leductrungxf@gmail.com\"},\"main\":\"dist/index.js\",\"repository\":{\"type\":\"git\",\"url\":\"https://github.com//jupyter_vtk\"},\"scripts\":{\"build\":\"npm run build:lib && npm run build:nbextension\",\"build:labextension\":\"npm run clean:labextension && mkdirp jupyter_vtk/labextension && cd jupyter_vtk/labextension && npm pack ../..\",\"build:lib\":\"tsc\",\"build:nbextension\":\"webpack --mode development\",\"build:all\":\"npm run build:labextension && npm run build:nbextension\",\"clean\":\"npm run clean:lib && npm run clean:nbextension\",\"clean:lib\":\"rimraf lib\",\"clean:labextension\":\"rimraf jupyter_vtk/labextension\",\"clean:nbextension\":\"rimraf jupyter_vtk/nbextension/static/index.js\",\"prepack\":\"npm run build:lib\",\"test\":\"npm run test:firefox\",\"test:chrome\":\"karma start --browsers=Chrome tests/karma.conf.js\",\"test:debug\":\"karma start --browsers=Chrome --singleRun=false --debug=true tests/karma.conf.js\",\"test:firefox\":\"karma start --browsers=Firefox tests/karma.conf.js\",\"test:ie\":\"karma start --browsers=IE tests/karma.conf.js\",\"watch\":\"npm-run-all -p watch:*\",\"watch:lib\":\"tsc -w\",\"watch:nbextension\":\"webpack --watch\"},\"dependencies\":{\"@blueprintjs/core\":\"^3.25.0\",\"itk\":\"^12.0.0\",\"re-resizable\":\"^6.3.2\",\"semantic-ui-react\":\"^0.88.2\",\"vtk.js\":\"^13.12.3\"},\"devDependencies\":{\"@babel/core\":\"^7.9.0\",\"@babel/preset-env\":\"^7.9.0\",\"@jupyter-widgets/base\":\"^3.0.0\",\"@jupyter-widgets/controls\":\"^2.0.0\",\"@jupyter-widgets/jupyterlab-manager\":\"^2.0.0\",\"@jupyterlab/application\":\"^2.1.0\",\"@jupyterlab/apputils\":\"^2.1.0\",\"@jupyterlab/notebook\":\"^2.1.0\",\"@lumino/application\":\"^1.8.4\",\"@lumino/widgets\":\"^1.11.1\",\"@types/expect.js\":\"^0.3.29\",\"@types/mocha\":\"^5.2.5\",\"@types/node\":\"^10.11.6\",\"@types/webpack-env\":\"^1.13.6\",\"autoprefixer\":\"^9.7.5\",\"babel-loader\":\"^8.1.0\",\"copy-webpack-plugin\":\"^5.1.1\",\"css-loader\":\"^3.2.0\",\"expect.js\":\"^0.3.1\",\"file-loader\":\"^6.0.0\",\"fs-extra\":\"^7.0.0\",\"karma\":\"^3.0.0\",\"karma-chrome-launcher\":\"^2.2.0\",\"karma-firefox-launcher\":\"^1.1.0\",\"karma-ie-launcher\":\"^1.0.0\",\"karma-mocha\":\"^1.3.0\",\"karma-mocha-reporter\":\"^2.2.5\",\"karma-typescript\":\"^3.0.13\",\"mkdirp\":\"^0.5.1\",\"mocha\":\"^5.2.0\",\"npm-run-all\":\"^4.1.3\",\"react\":\"^16.13.1\",\"rimraf\":\"^2.6.2\",\"shader-loader\":\"^1.3.1\",\"source-map-loader\":\"^0.2.4\",\"style-loader\":\"^1.0.0\",\"ts-loader\":\"^5.2.1\",\"typescript\":\"~3.1.2\",\"url-loader\":\"^4.1.0\",\"webpack\":\"^4.20.2\",\"webpack-cli\":\"^3.1.2\"},\"jupyterlab\":{\"extension\":\"dist/index\"}}");

/***/ }),

/***/ "./src/index.ts":
/*!**********************!*\
  !*** ./src/index.ts ***!
  \**********************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Trung Le
// Distributed under the terms of the Modified BSD License.
function __export(m) {
    for (var p in m) if (!exports.hasOwnProperty(p)) exports[p] = m[p];
}
Object.defineProperty(exports, "__esModule", { value: true });
__export(__webpack_require__(/*! ./version */ "./src/version.ts"));
// export * from './widget';


/***/ }),

/***/ "./src/version.ts":
/*!************************!*\
  !*** ./src/version.ts ***!
  \************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Trung Le
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", { value: true });
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;


/***/ })

/******/ })});;
//# sourceMappingURL=embed-bundle.js.map