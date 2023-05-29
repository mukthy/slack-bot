/******/ (function(modules) { // webpackBootstrap
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
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
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
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 20);
/******/ })
/************************************************************************/
/******/ ({

/***/ 1:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (immutable) */ __webpack_exports__["a"] = addJsonRpcListener;
/* harmony export (immutable) */ __webpack_exports__["b"] = callJsonRpc;
//Chrome extensions have an obnoxious amount of diff contexts
// * Content Page: can only use `chrome.runtime.sendMessage`
// * Background Page: Can use all methods. Needs to proxy messages from the devtools_page to content pages.
// * UI Pages: Can use all methods? (need to confirm chrome.tabs)
// * devtools_page: Does not have access to chrome.tabs so must proxy communication to content pages through background page. Can listen to messages not to a specific tab with `chrome.runtime.onMessage`.
// * devtools panel: Does not have access to chrome.tabs so must proxy communication to content pages through background page. Can listen to messages not to a specific tab with `chrome.runtime.onMessage`.

/**
 * Registers a method that is callable from other chrome extension contexts
 * @param {*} methodName the name of the method to register
 * @param {*} handler a function to be called when the method is called.
 *    Note: An additional argument, the senders tab id (or null if sender does not have tab id) will be will be appended to the arguments when calling the handler
 */
function addJsonRpcListener(methodName, handler) {
  chrome.runtime.onMessage.addListener(function(request, sender) {
    // Check if the call is for this listener
    if (request.method != methodName) {
      return;
    }

    var params = request.params || []
    params.push((sender.tab && sender.tab.id!=-1 && sender.tab.id) || null)
    var ret = handler.apply(null, params);
    if (!(ret || {}).then) {
      ret = Promise.resolve(ret);
    }
    ret.then(
      function(result) {
        if (sender.tab && sender.tab.id !== -1 && chrome.tabs) { //chrome.tabs is not defined in devtools && devtools sender.tab.id == -1
          chrome.tabs.sendMessage(sender.tab.id, { error: null, result: result, id: request.id });
        } else {
          chrome.runtime.sendMessage({ error: null, result: result, id: request.id });
        }
      },
      function(error) {
        if (sender.tab && sender.tab.id !== -1  && chrome.tabs) {
          chrome.tabs.sendMessage(sender.tab.id, { error: error, result: null, id: request.id });
        } else {
          chrome.runtime.sendMessage({ error: error, result: null, id: request.id });
        }
      }
    );
  });
}

/**
 * Calls a method in another chrome context that has been registered with addJsonRpcListener
 * @param {*} tabId the tab to send the message to. Pass null to send the message to a non tab recipient (aka background page)
 * @param {*} method the name of the method to call
 * @param {*} params arguments to pass to the method as additional params
 */
function callJsonRpc(tabId, method, params) {
  params = Array.from(arguments).splice(2)
  return new Promise(function(resolve, reject) {
    var id = Math.random();

    function cb(request) {
      if (request.id !== id) return; //its not us... ignore
      chrome.runtime.onMessage.removeListener(cb);
      if (request.error) { reject(request.error) } else { resolve(request.result) }
    }
    chrome.runtime.onMessage.addListener(cb)
    if (tabId) {
      chrome.tabs.sendMessage(tabId, { method: method, params: params, id: id });
    } else {
      chrome.runtime.sendMessage({ method: method, params: params, id: id });
    }
  });
}


/***/ }),

/***/ 20:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__messaging__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_file_loader_name_name_ext_dfpm_devtools_html__ = __webpack_require__(21);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_file_loader_name_name_ext_dfpm_devtools_html___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1_file_loader_name_name_ext_dfpm_devtools_html__);




var panelPromise = (new Promise((resolve,reject)=>
    chrome.devtools.panels.create("DFPM", "fake.png", "dfpm_panel.html", resolve)
))

Object(__WEBPACK_IMPORTED_MODULE_0__messaging__["b" /* callJsonRpc */])(null, 'registerDevtoolsTab', chrome.devtools.inspectedWindow.tabId)


/***/ }),

/***/ 21:
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__.p + "dfpm_devtools.html";

/***/ })

/******/ });