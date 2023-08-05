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
/******/ 	return __webpack_require__(__webpack_require__.s = 0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _hat_core_renderer__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(1);
/* harmony import */ var _hat_core_util__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(11);
/* harmony import */ var _hat_core_juggler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(12);
/* harmony import */ var orchestrator_main_scss__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(28);
/* harmony import */ var orchestrator_main_scss__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(orchestrator_main_scss__WEBPACK_IMPORTED_MODULE_3__);








const defaultState = {
    remote: null
};


let app = null;


function main() {
    const root = document.body.appendChild(document.createElement('div'));
    _hat_core_renderer__WEBPACK_IMPORTED_MODULE_0__["default"].init(root, defaultState, vt);
    app = new _hat_core_juggler__WEBPACK_IMPORTED_MODULE_2__["Application"](_hat_core_renderer__WEBPACK_IMPORTED_MODULE_0__["default"], null, null, 'remote');
}


function vt() {
    const remote = _hat_core_renderer__WEBPACK_IMPORTED_MODULE_0__["default"].get('remote');
    if (remote == null) return ['div'];

    const components = _hat_core_renderer__WEBPACK_IMPORTED_MODULE_0__["default"].get('remote', 'components');
    return ['div.orchestrator',
        ['table',
            ['thead',
                ['tr',
                    ['th.col-component', 'Component'],
                    ['th.col-delay', 'Delay'],
                    ['th.col-revive', 'Revive'],
                    ['th.col-status', 'Status'],
                    ['th.col-action', 'Action']
                ]
            ],
            ['tbody', components.map(component =>
                ['tr',
                    ['td.col-component', component.name],
                    ['td.col-delay', String(component.delay)],
                    ['td.col-revive',
                        ['input', {
                            props: {
                                type: 'checkbox',
                                checked: component.revive
                            },
                            on: {
                                change: evt => app.send({
                                    type: 'revive',
                                    payload: {
                                        id: component.id,
                                        value: evt.target.checked
                                    }
                                })
                            }}
                        ]
                    ],
                    ['td.col-status', component.status],
                    ['td.col-action',
                        ['button', {
                            props: {
                                title: 'Stop',
                                disabled: _hat_core_util__WEBPACK_IMPORTED_MODULE_1__["contains"](
                                    component.status, ['STOPPING', 'STOPPED'])
                            },
                            on: {
                                click: () => app.send({
                                    type: 'stop',
                                    payload: { id: component.id }
                                })
                            }},
                            ['span.fa.fa-times']
                        ],
                        ['button', {
                            props: {
                                title: 'Start',
                                disabled: _hat_core_util__WEBPACK_IMPORTED_MODULE_1__["contains"](
                                    component.status,
                                    ['STARTING', 'RUNNING', 'STOPPING'])
                            },
                            on: {
                                click: () => app.send({
                                    type: 'start',
                                    payload: { id: component.id }
                                })
                            }},
                            ['span.fa.fa-play']
                        ]
                    ]
                ]
            )]
        ]
    ];
}


window.addEventListener('load', main);
window.r = _hat_core_renderer__WEBPACK_IMPORTED_MODULE_0__["default"];
window.u = _hat_core_util__WEBPACK_IMPORTED_MODULE_1__;


/***/ }),
/* 1 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Renderer", function() { return Renderer; });
/* harmony import */ var snabbdom_es_snabbdom__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(2);
/* harmony import */ var snabbdom_es_modules_class__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(8);
/* harmony import */ var snabbdom_es_modules_dataset__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(9);
/* harmony import */ var snabbdom_es_modules_eventlisteners__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(10);
/* harmony import */ var _hat_core_util__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(11);
/** @module "@hat-core"/renderer
 */









// patched version of snabbdom's es/modules/attributes.js
const snabbdomAttributes = (() => {
    function updateAttrs(oldVnode, vnode) {
        var key, elm = vnode.elm, oldAttrs = oldVnode.data.attrs, attrs = vnode.data.attrs;
        if (!oldAttrs && !attrs)
            return;
        if (oldAttrs === attrs)
            return;
        oldAttrs = oldAttrs || {};
        attrs = attrs || {};
        for (key in attrs) {
            var cur = attrs[key];
            var old = oldAttrs[key];
            if (old !== cur) {
                if (cur === true) {
                    elm.setAttribute(key, "");
                }
                else if (cur === false) {
                    elm.removeAttribute(key);
                }
                else {
                    elm.setAttribute(key, cur);
                }
            }
        }
        for (key in oldAttrs) {
            if (!(key in attrs)) {
                elm.removeAttribute(key);
            }
        }
    }
    return { create: updateAttrs, update: updateAttrs };
})();


// patched version of snabbdom's es/modules/props.js
const snabbdomProps = (() => {
    function updateProps(oldVnode, vnode) {
        var key, cur, old, elm = vnode.elm, oldProps = oldVnode.data.props, props = vnode.data.props;
        if (!oldProps && !props)
            return;
        if (oldProps === props)
            return;
        oldProps = oldProps || {};
        props = props || {};
        for (key in oldProps) {
            if (!props[key]) {
                if (key === 'style') {
                    elm[key] = '';
                } else {
                    delete elm[key];
                }
            }
        }
        for (key in props) {
            cur = props[key];
            old = oldProps[key];
            if (old !== cur && (key !== 'value' || elm[key] !== cur)) {
                elm[key] = cur;
            }
        }
    }
    return { create: updateProps, update: updateProps };
})();


const patch = snabbdom_es_snabbdom__WEBPACK_IMPORTED_MODULE_0__["init"]([
    snabbdomAttributes,
    snabbdom_es_modules_class__WEBPACK_IMPORTED_MODULE_1__["default"],
    snabbdomProps,
    snabbdom_es_modules_dataset__WEBPACK_IMPORTED_MODULE_2__["default"],
    snabbdom_es_modules_eventlisteners__WEBPACK_IMPORTED_MODULE_3__["default"]
]);


function vhFromArray(node) {
    if (!node)
        return [];
    if (_hat_core_util__WEBPACK_IMPORTED_MODULE_4__["isString"](node))
        return node;
    if (!_hat_core_util__WEBPACK_IMPORTED_MODULE_4__["isArray"](node))
        throw 'Invalid node structure';
    if (node.length < 1)
        return [];
    if (typeof node[0] != 'string')
        return node.map(vhFromArray);
    const hasData = node.length > 1 && _hat_core_util__WEBPACK_IMPORTED_MODULE_4__["isObject"](node[1]);
    const children = _hat_core_util__WEBPACK_IMPORTED_MODULE_4__["pipe"](
        _hat_core_util__WEBPACK_IMPORTED_MODULE_4__["map"](vhFromArray),
        _hat_core_util__WEBPACK_IMPORTED_MODULE_4__["flatten"],
        Array.from
    )(node.slice(hasData ? 2 : 1));
    const result = hasData ?
        snabbdom_es_snabbdom__WEBPACK_IMPORTED_MODULE_0__["h"](node[0], node[1], children) :
        snabbdom_es_snabbdom__WEBPACK_IMPORTED_MODULE_0__["h"](node[0], children);
    return result;
}

/**
 * Virtual DOM renderer
 */
class Renderer extends EventTarget {

    /**
     * Calls `init` method
     * @param {HTMLElement} [el=document.body]
     * @param {Any} [initState=null]
     * @param {Function} [vtCb=null]
     * @param {Number} [maxFps=30]
     */
    constructor(el, initState, vtCb, maxFps) {
        super();
        this.init(el, initState, vtCb, maxFps);
    }

    /**
     * Initialize renderer
     * @param {HTMLElement} [el=document.body]
     * @param {Any} [initState=null]
     * @param {Function} [vtCb=null]
     * @param {Number} [maxFps=30]
     * @return {Promise}
     */
    init(el, initState, vtCb, maxFps) {
        this._state = null;
        this._changes = [];
        this._promise = null;
        this._timeout = null;
        this._lastRender = null;
        this._vtCb = vtCb;
        this._maxFps = _hat_core_util__WEBPACK_IMPORTED_MODULE_4__["isNumber"](maxFps) ? maxFps : 30;
        this._vNode = el || document.querySelector('body');
        if (initState)
            return this.change(_ => initState);
        return new Promise(resolve => { resolve(); });
    }

    /**
      * Render
      */
    render() {
        if (!this._vtCb)
            return;
        this._lastRender = performance.now();
        const vNode = vhFromArray(this._vtCb(this));
        patch(this._vNode, vNode);
        this._vNode = vNode;
        this.dispatchEvent(new CustomEvent('render', {detail: this._state}));
    }

    /**
     * Get current state value referenced by `paths`
     * @param {...Path} paths
     * @return {Any}
     */
    get(...paths) {
        return _hat_core_util__WEBPACK_IMPORTED_MODULE_4__["get"](paths, this._state);
    }

    /**
     * Change current state value referenced by `path`
     * @param {Path} path
     * @param {Any} value
     * @return {Promise}
     */
    set(path, value) {
        if (arguments.length < 2) {
            value = path;
            path = [];
        }
        return this.change(path, _ => value);
    }

    /**
     * Change current state value referenced by `path`
     * @param {Path} path
     * @param {Function} cb
     * @return {Promise}
     */
    change(path, cb) {
        if (arguments.length < 2) {
            cb = path;
            path = [];
        }
        this._changes.push([path, cb]);
        if (this._promise)
            return this._promise;
        this._promise = new Promise((resolve, reject) => {
            setTimeout(() => {
                try {
                    this._change();
                } catch(e) {
                    this._promise = null;
                    reject(e);
                    throw e;
                }
                this._promise = null;
                resolve();
            }, 0);
        });
        return this._promise;
    }

    _change() {
        let change = false;
        while (this._changes.length > 0) {
            const [path, cb] = this._changes.shift();
            const view = _hat_core_util__WEBPACK_IMPORTED_MODULE_4__["get"](path);
            const oldState = this._state;
            this._state = _hat_core_util__WEBPACK_IMPORTED_MODULE_4__["change"](path, cb, this._state);
            if (this._state && _hat_core_util__WEBPACK_IMPORTED_MODULE_4__["equals"](view(oldState),
                                        view(this._state)))
                continue;
            change = true;
            if (!this._vtCb || this._timeout)
                continue;
            const delay = (!this._lastRender || !this._maxFps ?
                0 :
                (1000 / this._maxFps) -
                (performance.now() - this._lastRender));
            this._timeout = setTimeout(() => {
                this._timeout = null;
                this.render();
            }, (delay > 0 ? delay : 0));
        }
        if (change)
            this.dispatchEvent(
                new CustomEvent('change', {detail: this._state}));
    }
}
// Renderer.prototype.set = u.curry(Renderer.prototype.set);
// Renderer.prototype.change = u.curry(Renderer.prototype.change);


/**
 * Default renderer
 * @static
 * @type {Renderer}
 */
const defaultRenderer = (() => {
    const r = (window && window.__hat_default_renderer) || new Renderer();
    if (window)
        window.__hat_default_renderer = r;
    return r;
})();
/* harmony default export */ __webpack_exports__["default"] = (defaultRenderer);


/***/ }),
/* 2 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "init", function() { return init; });
/* harmony import */ var _vnode__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(3);
/* harmony import */ var _is__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(4);
/* harmony import */ var _htmldomapi__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(5);
/* harmony import */ var _h__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(6);
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "h", function() { return _h__WEBPACK_IMPORTED_MODULE_3__["h"]; });

/* harmony import */ var _thunk__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(7);
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "thunk", function() { return _thunk__WEBPACK_IMPORTED_MODULE_4__["thunk"]; });




function isUndef(s) { return s === undefined; }
function isDef(s) { return s !== undefined; }
var emptyNode = Object(_vnode__WEBPACK_IMPORTED_MODULE_0__["default"])('', {}, [], undefined, undefined);
function sameVnode(vnode1, vnode2) {
    return vnode1.key === vnode2.key && vnode1.sel === vnode2.sel;
}
function isVnode(vnode) {
    return vnode.sel !== undefined;
}
function createKeyToOldIdx(children, beginIdx, endIdx) {
    var i, map = {}, key, ch;
    for (i = beginIdx; i <= endIdx; ++i) {
        ch = children[i];
        if (ch != null) {
            key = ch.key;
            if (key !== undefined)
                map[key] = i;
        }
    }
    return map;
}
var hooks = ['create', 'update', 'remove', 'destroy', 'pre', 'post'];


function init(modules, domApi) {
    var i, j, cbs = {};
    var api = domApi !== undefined ? domApi : _htmldomapi__WEBPACK_IMPORTED_MODULE_2__["default"];
    for (i = 0; i < hooks.length; ++i) {
        cbs[hooks[i]] = [];
        for (j = 0; j < modules.length; ++j) {
            var hook = modules[j][hooks[i]];
            if (hook !== undefined) {
                cbs[hooks[i]].push(hook);
            }
        }
    }
    function emptyNodeAt(elm) {
        var id = elm.id ? '#' + elm.id : '';
        var c = elm.className ? '.' + elm.className.split(' ').join('.') : '';
        return Object(_vnode__WEBPACK_IMPORTED_MODULE_0__["default"])(api.tagName(elm).toLowerCase() + id + c, {}, [], undefined, elm);
    }
    function createRmCb(childElm, listeners) {
        return function rmCb() {
            if (--listeners === 0) {
                var parent_1 = api.parentNode(childElm);
                api.removeChild(parent_1, childElm);
            }
        };
    }
    function createElm(vnode, insertedVnodeQueue) {
        var i, data = vnode.data;
        if (data !== undefined) {
            if (isDef(i = data.hook) && isDef(i = i.init)) {
                i(vnode);
                data = vnode.data;
            }
        }
        var children = vnode.children, sel = vnode.sel;
        if (sel === '!') {
            if (isUndef(vnode.text)) {
                vnode.text = '';
            }
            vnode.elm = api.createComment(vnode.text);
        }
        else if (sel !== undefined) {
            // Parse selector
            var hashIdx = sel.indexOf('#');
            var dotIdx = sel.indexOf('.', hashIdx);
            var hash = hashIdx > 0 ? hashIdx : sel.length;
            var dot = dotIdx > 0 ? dotIdx : sel.length;
            var tag = hashIdx !== -1 || dotIdx !== -1 ? sel.slice(0, Math.min(hash, dot)) : sel;
            var elm = vnode.elm = isDef(data) && isDef(i = data.ns) ? api.createElementNS(i, tag)
                : api.createElement(tag);
            if (hash < dot)
                elm.setAttribute('id', sel.slice(hash + 1, dot));
            if (dotIdx > 0)
                elm.setAttribute('class', sel.slice(dot + 1).replace(/\./g, ' '));
            for (i = 0; i < cbs.create.length; ++i)
                cbs.create[i](emptyNode, vnode);
            if (_is__WEBPACK_IMPORTED_MODULE_1__["array"](children)) {
                for (i = 0; i < children.length; ++i) {
                    var ch = children[i];
                    if (ch != null) {
                        api.appendChild(elm, createElm(ch, insertedVnodeQueue));
                    }
                }
            }
            else if (_is__WEBPACK_IMPORTED_MODULE_1__["primitive"](vnode.text)) {
                api.appendChild(elm, api.createTextNode(vnode.text));
            }
            i = vnode.data.hook; // Reuse variable
            if (isDef(i)) {
                if (i.create)
                    i.create(emptyNode, vnode);
                if (i.insert)
                    insertedVnodeQueue.push(vnode);
            }
        }
        else {
            vnode.elm = api.createTextNode(vnode.text);
        }
        return vnode.elm;
    }
    function addVnodes(parentElm, before, vnodes, startIdx, endIdx, insertedVnodeQueue) {
        for (; startIdx <= endIdx; ++startIdx) {
            var ch = vnodes[startIdx];
            if (ch != null) {
                api.insertBefore(parentElm, createElm(ch, insertedVnodeQueue), before);
            }
        }
    }
    function invokeDestroyHook(vnode) {
        var i, j, data = vnode.data;
        if (data !== undefined) {
            if (isDef(i = data.hook) && isDef(i = i.destroy))
                i(vnode);
            for (i = 0; i < cbs.destroy.length; ++i)
                cbs.destroy[i](vnode);
            if (vnode.children !== undefined) {
                for (j = 0; j < vnode.children.length; ++j) {
                    i = vnode.children[j];
                    if (i != null && typeof i !== "string") {
                        invokeDestroyHook(i);
                    }
                }
            }
        }
    }
    function removeVnodes(parentElm, vnodes, startIdx, endIdx) {
        for (; startIdx <= endIdx; ++startIdx) {
            var i_1 = void 0, listeners = void 0, rm = void 0, ch = vnodes[startIdx];
            if (ch != null) {
                if (isDef(ch.sel)) {
                    invokeDestroyHook(ch);
                    listeners = cbs.remove.length + 1;
                    rm = createRmCb(ch.elm, listeners);
                    for (i_1 = 0; i_1 < cbs.remove.length; ++i_1)
                        cbs.remove[i_1](ch, rm);
                    if (isDef(i_1 = ch.data) && isDef(i_1 = i_1.hook) && isDef(i_1 = i_1.remove)) {
                        i_1(ch, rm);
                    }
                    else {
                        rm();
                    }
                }
                else { // Text node
                    api.removeChild(parentElm, ch.elm);
                }
            }
        }
    }
    function updateChildren(parentElm, oldCh, newCh, insertedVnodeQueue) {
        var oldStartIdx = 0, newStartIdx = 0;
        var oldEndIdx = oldCh.length - 1;
        var oldStartVnode = oldCh[0];
        var oldEndVnode = oldCh[oldEndIdx];
        var newEndIdx = newCh.length - 1;
        var newStartVnode = newCh[0];
        var newEndVnode = newCh[newEndIdx];
        var oldKeyToIdx;
        var idxInOld;
        var elmToMove;
        var before;
        while (oldStartIdx <= oldEndIdx && newStartIdx <= newEndIdx) {
            if (oldStartVnode == null) {
                oldStartVnode = oldCh[++oldStartIdx]; // Vnode might have been moved left
            }
            else if (oldEndVnode == null) {
                oldEndVnode = oldCh[--oldEndIdx];
            }
            else if (newStartVnode == null) {
                newStartVnode = newCh[++newStartIdx];
            }
            else if (newEndVnode == null) {
                newEndVnode = newCh[--newEndIdx];
            }
            else if (sameVnode(oldStartVnode, newStartVnode)) {
                patchVnode(oldStartVnode, newStartVnode, insertedVnodeQueue);
                oldStartVnode = oldCh[++oldStartIdx];
                newStartVnode = newCh[++newStartIdx];
            }
            else if (sameVnode(oldEndVnode, newEndVnode)) {
                patchVnode(oldEndVnode, newEndVnode, insertedVnodeQueue);
                oldEndVnode = oldCh[--oldEndIdx];
                newEndVnode = newCh[--newEndIdx];
            }
            else if (sameVnode(oldStartVnode, newEndVnode)) { // Vnode moved right
                patchVnode(oldStartVnode, newEndVnode, insertedVnodeQueue);
                api.insertBefore(parentElm, oldStartVnode.elm, api.nextSibling(oldEndVnode.elm));
                oldStartVnode = oldCh[++oldStartIdx];
                newEndVnode = newCh[--newEndIdx];
            }
            else if (sameVnode(oldEndVnode, newStartVnode)) { // Vnode moved left
                patchVnode(oldEndVnode, newStartVnode, insertedVnodeQueue);
                api.insertBefore(parentElm, oldEndVnode.elm, oldStartVnode.elm);
                oldEndVnode = oldCh[--oldEndIdx];
                newStartVnode = newCh[++newStartIdx];
            }
            else {
                if (oldKeyToIdx === undefined) {
                    oldKeyToIdx = createKeyToOldIdx(oldCh, oldStartIdx, oldEndIdx);
                }
                idxInOld = oldKeyToIdx[newStartVnode.key];
                if (isUndef(idxInOld)) { // New element
                    api.insertBefore(parentElm, createElm(newStartVnode, insertedVnodeQueue), oldStartVnode.elm);
                    newStartVnode = newCh[++newStartIdx];
                }
                else {
                    elmToMove = oldCh[idxInOld];
                    if (elmToMove.sel !== newStartVnode.sel) {
                        api.insertBefore(parentElm, createElm(newStartVnode, insertedVnodeQueue), oldStartVnode.elm);
                    }
                    else {
                        patchVnode(elmToMove, newStartVnode, insertedVnodeQueue);
                        oldCh[idxInOld] = undefined;
                        api.insertBefore(parentElm, elmToMove.elm, oldStartVnode.elm);
                    }
                    newStartVnode = newCh[++newStartIdx];
                }
            }
        }
        if (oldStartIdx <= oldEndIdx || newStartIdx <= newEndIdx) {
            if (oldStartIdx > oldEndIdx) {
                before = newCh[newEndIdx + 1] == null ? null : newCh[newEndIdx + 1].elm;
                addVnodes(parentElm, before, newCh, newStartIdx, newEndIdx, insertedVnodeQueue);
            }
            else {
                removeVnodes(parentElm, oldCh, oldStartIdx, oldEndIdx);
            }
        }
    }
    function patchVnode(oldVnode, vnode, insertedVnodeQueue) {
        var i, hook;
        if (isDef(i = vnode.data) && isDef(hook = i.hook) && isDef(i = hook.prepatch)) {
            i(oldVnode, vnode);
        }
        var elm = vnode.elm = oldVnode.elm;
        var oldCh = oldVnode.children;
        var ch = vnode.children;
        if (oldVnode === vnode)
            return;
        if (vnode.data !== undefined) {
            for (i = 0; i < cbs.update.length; ++i)
                cbs.update[i](oldVnode, vnode);
            i = vnode.data.hook;
            if (isDef(i) && isDef(i = i.update))
                i(oldVnode, vnode);
        }
        if (isUndef(vnode.text)) {
            if (isDef(oldCh) && isDef(ch)) {
                if (oldCh !== ch)
                    updateChildren(elm, oldCh, ch, insertedVnodeQueue);
            }
            else if (isDef(ch)) {
                if (isDef(oldVnode.text))
                    api.setTextContent(elm, '');
                addVnodes(elm, null, ch, 0, ch.length - 1, insertedVnodeQueue);
            }
            else if (isDef(oldCh)) {
                removeVnodes(elm, oldCh, 0, oldCh.length - 1);
            }
            else if (isDef(oldVnode.text)) {
                api.setTextContent(elm, '');
            }
        }
        else if (oldVnode.text !== vnode.text) {
            if (isDef(oldCh)) {
                removeVnodes(elm, oldCh, 0, oldCh.length - 1);
            }
            api.setTextContent(elm, vnode.text);
        }
        if (isDef(hook) && isDef(i = hook.postpatch)) {
            i(oldVnode, vnode);
        }
    }
    return function patch(oldVnode, vnode) {
        var i, elm, parent;
        var insertedVnodeQueue = [];
        for (i = 0; i < cbs.pre.length; ++i)
            cbs.pre[i]();
        if (!isVnode(oldVnode)) {
            oldVnode = emptyNodeAt(oldVnode);
        }
        if (sameVnode(oldVnode, vnode)) {
            patchVnode(oldVnode, vnode, insertedVnodeQueue);
        }
        else {
            elm = oldVnode.elm;
            parent = api.parentNode(elm);
            createElm(vnode, insertedVnodeQueue);
            if (parent !== null) {
                api.insertBefore(parent, vnode.elm, api.nextSibling(elm));
                removeVnodes(parent, [oldVnode], 0, 0);
            }
        }
        for (i = 0; i < insertedVnodeQueue.length; ++i) {
            insertedVnodeQueue[i].data.hook.insert(insertedVnodeQueue[i]);
        }
        for (i = 0; i < cbs.post.length; ++i)
            cbs.post[i]();
        return vnode;
    };
}
//# sourceMappingURL=snabbdom.js.map

/***/ }),
/* 3 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "vnode", function() { return vnode; });
function vnode(sel, data, children, text, elm) {
    var key = data === undefined ? undefined : data.key;
    return { sel: sel, data: data, children: children, text: text, elm: elm, key: key };
}
/* harmony default export */ __webpack_exports__["default"] = (vnode);
//# sourceMappingURL=vnode.js.map

/***/ }),
/* 4 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "array", function() { return array; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "primitive", function() { return primitive; });
var array = Array.isArray;
function primitive(s) {
    return typeof s === 'string' || typeof s === 'number';
}
//# sourceMappingURL=is.js.map

/***/ }),
/* 5 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "htmlDomApi", function() { return htmlDomApi; });
function createElement(tagName) {
    return document.createElement(tagName);
}
function createElementNS(namespaceURI, qualifiedName) {
    return document.createElementNS(namespaceURI, qualifiedName);
}
function createTextNode(text) {
    return document.createTextNode(text);
}
function createComment(text) {
    return document.createComment(text);
}
function insertBefore(parentNode, newNode, referenceNode) {
    parentNode.insertBefore(newNode, referenceNode);
}
function removeChild(node, child) {
    node.removeChild(child);
}
function appendChild(node, child) {
    node.appendChild(child);
}
function parentNode(node) {
    return node.parentNode;
}
function nextSibling(node) {
    return node.nextSibling;
}
function tagName(elm) {
    return elm.tagName;
}
function setTextContent(node, text) {
    node.textContent = text;
}
function getTextContent(node) {
    return node.textContent;
}
function isElement(node) {
    return node.nodeType === 1;
}
function isText(node) {
    return node.nodeType === 3;
}
function isComment(node) {
    return node.nodeType === 8;
}
var htmlDomApi = {
    createElement: createElement,
    createElementNS: createElementNS,
    createTextNode: createTextNode,
    createComment: createComment,
    insertBefore: insertBefore,
    removeChild: removeChild,
    appendChild: appendChild,
    parentNode: parentNode,
    nextSibling: nextSibling,
    tagName: tagName,
    setTextContent: setTextContent,
    getTextContent: getTextContent,
    isElement: isElement,
    isText: isText,
    isComment: isComment,
};
/* harmony default export */ __webpack_exports__["default"] = (htmlDomApi);
//# sourceMappingURL=htmldomapi.js.map

/***/ }),
/* 6 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "h", function() { return h; });
/* harmony import */ var _vnode__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(3);
/* harmony import */ var _is__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(4);


function addNS(data, children, sel) {
    data.ns = 'http://www.w3.org/2000/svg';
    if (sel !== 'foreignObject' && children !== undefined) {
        for (var i = 0; i < children.length; ++i) {
            var childData = children[i].data;
            if (childData !== undefined) {
                addNS(childData, children[i].children, children[i].sel);
            }
        }
    }
}
function h(sel, b, c) {
    var data = {}, children, text, i;
    if (c !== undefined) {
        data = b;
        if (_is__WEBPACK_IMPORTED_MODULE_1__["array"](c)) {
            children = c;
        }
        else if (_is__WEBPACK_IMPORTED_MODULE_1__["primitive"](c)) {
            text = c;
        }
        else if (c && c.sel) {
            children = [c];
        }
    }
    else if (b !== undefined) {
        if (_is__WEBPACK_IMPORTED_MODULE_1__["array"](b)) {
            children = b;
        }
        else if (_is__WEBPACK_IMPORTED_MODULE_1__["primitive"](b)) {
            text = b;
        }
        else if (b && b.sel) {
            children = [b];
        }
        else {
            data = b;
        }
    }
    if (children !== undefined) {
        for (i = 0; i < children.length; ++i) {
            if (_is__WEBPACK_IMPORTED_MODULE_1__["primitive"](children[i]))
                children[i] = Object(_vnode__WEBPACK_IMPORTED_MODULE_0__["vnode"])(undefined, undefined, undefined, children[i], undefined);
        }
    }
    if (sel[0] === 's' && sel[1] === 'v' && sel[2] === 'g' &&
        (sel.length === 3 || sel[3] === '.' || sel[3] === '#')) {
        addNS(data, children, sel);
    }
    return Object(_vnode__WEBPACK_IMPORTED_MODULE_0__["vnode"])(sel, data, children, text, undefined);
}
;
/* harmony default export */ __webpack_exports__["default"] = (h);
//# sourceMappingURL=h.js.map

/***/ }),
/* 7 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "thunk", function() { return thunk; });
/* harmony import */ var _h__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(6);

function copyToThunk(vnode, thunk) {
    thunk.elm = vnode.elm;
    vnode.data.fn = thunk.data.fn;
    vnode.data.args = thunk.data.args;
    thunk.data = vnode.data;
    thunk.children = vnode.children;
    thunk.text = vnode.text;
    thunk.elm = vnode.elm;
}
function init(thunk) {
    var cur = thunk.data;
    var vnode = cur.fn.apply(undefined, cur.args);
    copyToThunk(vnode, thunk);
}
function prepatch(oldVnode, thunk) {
    var i, old = oldVnode.data, cur = thunk.data;
    var oldArgs = old.args, args = cur.args;
    if (old.fn !== cur.fn || oldArgs.length !== args.length) {
        copyToThunk(cur.fn.apply(undefined, args), thunk);
        return;
    }
    for (i = 0; i < args.length; ++i) {
        if (oldArgs[i] !== args[i]) {
            copyToThunk(cur.fn.apply(undefined, args), thunk);
            return;
        }
    }
    copyToThunk(oldVnode, thunk);
}
var thunk = function thunk(sel, key, fn, args) {
    if (args === undefined) {
        args = fn;
        fn = key;
        key = undefined;
    }
    return Object(_h__WEBPACK_IMPORTED_MODULE_0__["h"])(sel, {
        key: key,
        hook: { init: init, prepatch: prepatch },
        fn: fn,
        args: args
    });
};
/* harmony default export */ __webpack_exports__["default"] = (thunk);
//# sourceMappingURL=thunk.js.map

/***/ }),
/* 8 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "classModule", function() { return classModule; });
function updateClass(oldVnode, vnode) {
    var cur, name, elm = vnode.elm, oldClass = oldVnode.data.class, klass = vnode.data.class;
    if (!oldClass && !klass)
        return;
    if (oldClass === klass)
        return;
    oldClass = oldClass || {};
    klass = klass || {};
    for (name in oldClass) {
        if (!klass[name]) {
            elm.classList.remove(name);
        }
    }
    for (name in klass) {
        cur = klass[name];
        if (cur !== oldClass[name]) {
            elm.classList[cur ? 'add' : 'remove'](name);
        }
    }
}
var classModule = { create: updateClass, update: updateClass };
/* harmony default export */ __webpack_exports__["default"] = (classModule);
//# sourceMappingURL=class.js.map

/***/ }),
/* 9 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "datasetModule", function() { return datasetModule; });
var CAPS_REGEX = /[A-Z]/g;
function updateDataset(oldVnode, vnode) {
    var elm = vnode.elm, oldDataset = oldVnode.data.dataset, dataset = vnode.data.dataset, key;
    if (!oldDataset && !dataset)
        return;
    if (oldDataset === dataset)
        return;
    oldDataset = oldDataset || {};
    dataset = dataset || {};
    var d = elm.dataset;
    for (key in oldDataset) {
        if (!dataset[key]) {
            if (d) {
                if (key in d) {
                    delete d[key];
                }
            }
            else {
                elm.removeAttribute('data-' + key.replace(CAPS_REGEX, '-$&').toLowerCase());
            }
        }
    }
    for (key in dataset) {
        if (oldDataset[key] !== dataset[key]) {
            if (d) {
                d[key] = dataset[key];
            }
            else {
                elm.setAttribute('data-' + key.replace(CAPS_REGEX, '-$&').toLowerCase(), dataset[key]);
            }
        }
    }
}
var datasetModule = { create: updateDataset, update: updateDataset };
/* harmony default export */ __webpack_exports__["default"] = (datasetModule);
//# sourceMappingURL=dataset.js.map

/***/ }),
/* 10 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "eventListenersModule", function() { return eventListenersModule; });
function invokeHandler(handler, vnode, event) {
    if (typeof handler === "function") {
        // call function handler
        handler.call(vnode, event, vnode);
    }
    else if (typeof handler === "object") {
        // call handler with arguments
        if (typeof handler[0] === "function") {
            // special case for single argument for performance
            if (handler.length === 2) {
                handler[0].call(vnode, handler[1], event, vnode);
            }
            else {
                var args = handler.slice(1);
                args.push(event);
                args.push(vnode);
                handler[0].apply(vnode, args);
            }
        }
        else {
            // call multiple handlers
            for (var i = 0; i < handler.length; i++) {
                invokeHandler(handler[i], vnode, event);
            }
        }
    }
}
function handleEvent(event, vnode) {
    var name = event.type, on = vnode.data.on;
    // call event handler(s) if exists
    if (on && on[name]) {
        invokeHandler(on[name], vnode, event);
    }
}
function createListener() {
    return function handler(event) {
        handleEvent(event, handler.vnode);
    };
}
function updateEventListeners(oldVnode, vnode) {
    var oldOn = oldVnode.data.on, oldListener = oldVnode.listener, oldElm = oldVnode.elm, on = vnode && vnode.data.on, elm = (vnode && vnode.elm), name;
    // optimization for reused immutable handlers
    if (oldOn === on) {
        return;
    }
    // remove existing listeners which no longer used
    if (oldOn && oldListener) {
        // if element changed or deleted we remove all existing listeners unconditionally
        if (!on) {
            for (name in oldOn) {
                // remove listener if element was changed or existing listeners removed
                oldElm.removeEventListener(name, oldListener, false);
            }
        }
        else {
            for (name in oldOn) {
                // remove listener if existing listener removed
                if (!on[name]) {
                    oldElm.removeEventListener(name, oldListener, false);
                }
            }
        }
    }
    // add new listeners which has not already attached
    if (on) {
        // reuse existing listener or create new
        var listener = vnode.listener = oldVnode.listener || createListener();
        // update vnode for listener
        listener.vnode = vnode;
        // if element changed or added we add all needed listeners unconditionally
        if (!oldOn) {
            for (name in on) {
                // add listener if element was changed or new listeners added
                elm.addEventListener(name, listener, false);
            }
        }
        else {
            for (name in on) {
                // add listener if new listener added
                if (!oldOn[name]) {
                    elm.addEventListener(name, listener, false);
                }
            }
        }
    }
}
var eventListenersModule = {
    create: updateEventListeners,
    update: updateEventListeners,
    destroy: updateEventListeners
};
/* harmony default export */ __webpack_exports__["default"] = (eventListenersModule);
//# sourceMappingURL=eventlisteners.js.map

/***/ }),
/* 11 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "identity", function() { return identity; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isArray", function() { return isArray; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isObject", function() { return isObject; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isNumber", function() { return isNumber; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isInteger", function() { return isInteger; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isString", function() { return isString; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "strictParseInt", function() { return strictParseInt; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "strictParseFloat", function() { return strictParseFloat; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "clone", function() { return clone; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "zip", function() { return zip; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "toPairs", function() { return toPairs; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "fromPairs", function() { return fromPairs; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "flatten", function() { return flatten; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "pipe", function() { return pipe; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "flap", function() { return flap; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "curry", function() { return curry; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "equals", function() { return equals; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "get", function() { return get; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "change", function() { return change; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "set", function() { return set; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "omit", function() { return omit; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "move", function() { return move; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "sortBy", function() { return sortBy; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "pick", function() { return pick; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "map", function() { return map; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "filter", function() { return filter; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "append", function() { return append; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "reduce", function() { return reduce; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "merge", function() { return merge; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "mergeAll", function() { return mergeAll; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "find", function() { return find; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "concat", function() { return concat; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "union", function() { return union; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "contains", function() { return contains; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "insert", function() { return insert; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "slice", function() { return slice; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "reverse", function() { return reverse; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "length", function() { return length; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "sleep", function() { return sleep; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "inc", function() { return inc; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "dec", function() { return dec; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "not", function() { return not; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "delay", function() { return delay; });
/** @module "@hat-core"/util
 */

/**
 * Path can be an object property name, array index, or array of Paths
 * @typedef {string|number|Path[]} module:"@hat-core"/util.Path
 */

/**
 * Identity function
 * @function
 * @param {Any} obj input object
 * @return {Any} same object as input
 */
const identity = obj => obj;

/**
 * Check if value is Array (wrapper for Array.isArray)
 * @function
 * @param {Any} arr input object
 * @return {Boolean}
 */
const isArray = Array.isArray;

/**
 * Check if value is Object (not `true` from Array or `null`)
 * @function
 * @param {Any} obj input object
 * @return {Boolean}
 */
const isObject = obj => obj !== null &&
                               typeof(obj) == 'object' &&
                               !isArray(obj);

/**
 * Check if value is number
 * @function
 * @param {Any} n input object
 * @return {Boolean}
 */
const isNumber = n => typeof(n) == 'number';

/**
 * Check if value is integer
 * @function
 * @param {Any} n input object
 * @type {Boolean}
 */
const isInteger = Number.isInteger;

/**
 * Check if value is string
 * @function
 * @param {Any} str input object
 * @type {Boolean}
 */
const isString = str => typeof(str) == 'string';

/**
 * Strictly parse integer from string
 * @param {String} value
 * @return {Number}
 */
function strictParseInt(value) {
    if (/^(-|\+)?([0-9]+)$/.test(value))
        return Number(value);
    return NaN;
}

/**
 * Strictly parse float from string
 * @param {String} value
 * @return {Number}
 */
function strictParseFloat(value) {
    if (/^(-|\+)?([0-9]+(\.[0-9]+)?)$/.test(value))
        return Number(value);
    return NaN;
}

/**
 * Create new deep copy of input value
 * @param {Any} value
 * @return {Any} copy of value
 */
function clone(obj) {
    if (isArray(obj))
        return Array.from(obj, clone);
    if (isObject(obj)) {
        let ret = {};
        for (let i in obj)
            ret[i] = clone(obj[i]);
        return ret;
    }
    return obj;
}

/**
 * Combine two arrays in single array of pairs
 * @param {Array<Any>} arr1
 * @param {Array<Any>} arr2
 * @return {Array<Array<Any>>}
 */
function zip(arr1, arr2) {
    return Array.from((function*() {
        for (let i = 0; i < arr1.length || i < arr2.length; ++i)
            yield [arr1[i], arr2[i]];
    })());
}

/**
 * Convert object to array of key, value pairs
 * @param {Object} obj
 * @return {Array<Array>}
 */
function toPairs(obj) {
    return Object.entries(obj);
}

/**
 * Convert array of key, value pairs to object
 * @param {Array<Array>} arr
 * @return {Object}
 */
function fromPairs(arr) {
    let ret = {};
    for (let [k, v] of arr)
        ret[k] = v;
    return ret;
}

/**
 * Flatten nested arrays
 * @param {Array} arr
 * @return {Generator}
 */
function* flatten(arr) {
    if (isArray(arr)) {
        for (let i of arr)
            if (isArray(i))
                yield* flatten(i);
            else
                yield i;
    } else {
        yield arr;
    }
}

/**
 * Pipe function calls (functional composition with reversed order)
 * @param {...Function} fns functions
 * @return {Function}
 */
function pipe(...fns) {
    if (fns.length < 1)
        throw 'no functions';
    return function (...args) {
        let ret = fns[0].apply(this, args);
        for (let fn of fns.slice(1))
            ret = fn(ret);
        return ret;
    };
}

/**
 * Apply list of functions to same arguments and return list of results
 * @param {...Function} fns functions
 * @return {Function}
 */
function flap(...fns) {
    return (...args) => fns.map(fn => fn.apply(this, args));
}

/**
 * Curry function with fixed arguments lenth
 * @param {Function} fn
 * @return {Function}
 */
function curry(fn) {
    let wrapper = function(oldArgs) {
        return function(...args) {
            args = oldArgs.concat(args);
            if (args.length >= fn.length)
                return fn(...args);
            return wrapper(args);
        };
    };
    return wrapper([]);
}

/**
 * Deep object equality
 * (curried function)
 * @function
 * @param {Any} x
 * @param {Any} y
 * @return {Boolean}
 */
const equals = curry((x, y) => {
    if (x === y)
        return true;
    if (typeof(x) != 'object' ||
        typeof(y) != 'object' ||
        x === null ||
        y === null)
        return false;
    if (Array.isArray(x) && Array.isArray(y)) {
        if (x.length != y.length)
            return false;
        for (let [a, b] of zip(x, y)) {
            if (!equals(a, b))
                return false;
        }
        return true;
    } else if (!Array.isArray(x) && !Array.isArray(y)) {
        if (Object.keys(x).length != Object.keys(y).length)
            return false;
        for (let key in x) {
            if (!(key in y))
                return false;
        }
        for (let key in x) {
            if (!equals(x[key], y[key]))
                return false;
        }
        return true;
    }
    return false;
});

/**
 * Get value from `obj` referenced by `path`
 * (curried function)
 * @function
 * @param {Path} path
 * @param {Any} obj
 * @return {Any}
 */
const get = curry((path, obj) => {
    let ret = obj;
    for (let i of flatten(path)) {
        if (ret === null || typeof(ret) != 'object')
            return undefined;
        ret = ret[i];
    }
    return ret;
});

/**
 * Change `obj` by appling function `fn` to value referenced by `path`
 * (curried function)
 * @function
 * @param {Path} path
 * @param {Function} fn
 * @param {Any} obj
 * @return {Any} changed `obj`
 */
const change = curry((path, fn, obj) => {
    function _change(path, obj) {
        if (isInteger(path[0])) {
            obj = (isArray(obj) ? Array.from(obj) : []);
        } else if (isString(path[0])) {
            obj = (isObject(obj) ? Object.assign({}, obj) : {});
        } else {
            throw 'invalid path';
        }
        if (path.length > 1) {
            obj[path[0]] = _change(path.slice(1), obj[path[0]]);
        } else {
            obj[path[0]] = fn(obj[path[0]]);
        }
        return obj;
    }
    path = Array.from(flatten(path));
    if (path.length < 1)
        return fn(obj);
    return _change(path, obj);
});

/**
 * Change `obj` by setting value referenced by `path` to `val`
 * (curried function)
 * @function
 * @param {Path} path
 * @param {Any} val
 * @param {Any} obj
 * @return {Any} changed `obj`
 */
const set = curry((path, val, obj) => change(path, _ => val, obj));

/**
 * Change `obj` by omitting value referenced by `path`
 * (curried function)
 * @function
 * @param {Path} path
 * @param {Any} obj
 * @return {Any} changed `obj`
 */
const omit = curry((path, obj) => {
    function _omit(path, obj) {
        if (isInteger(path[0])) {
            obj = (isArray(obj) ? Array.from(obj) : []);
        } else if (isString(path[0])) {
            obj = (isObject(obj) ? Object.assign({}, obj) : {});
        } else {
            throw 'invalid path';
        }
        if (path.length > 1) {
            obj[path[0]] = _omit(path.slice(1), obj[path[0]]);
        } else if (isInteger(path[0])) {
            obj.splice(path[0], 1);
        } else {
            delete obj[path[0]];
        }
        return obj;
    }
    path = Array.from(flatten(path));
    if (path.length < 1)
        return undefined;
    return _omit(path, obj);
});

/**
 * Change `obj` by moving value from `srcPath` to `dstPath`
 * (curried function)
 * @function
 * @param {Path} srcPath
 * @param {Path} dstPath
 * @param {Any} obj
 * @return {Any} changed `obj`
 */
const move = curry((srcPath, dstPath, obj) => pipe(
    set(dstPath, get(srcPath, obj)),
    omit(srcPath)
)(obj));

/**
 * Sort `arr` by with comparison function `fn`
 * (curried function)
 * @function
 * @param {Function} fn
 * @param {Array} arr
 * @return {Array} sorted `arr`
 */
const sortBy = curry((fn, arr) => Array.from(arr).sort((x, y) => {
    let xVal = fn(x);
    let yVal = fn(y);
    if (xVal < yVal)
        return -1;
    if (xVal > yVal)
        return 1;
    return 0;
}));

/**
 * Create object which is subset `obj` containing only properties defined by
 * `arr`
 * (curried function)
 * @function
 * @param {Array} arr
 * @param {Object} obj
 * @return {Object} subset of `obj`
 */
const pick = curry((arr, obj) => {
    const ret = {};
    for (let i of arr)
        if (i in obj)
            ret[i] = obj[i];
    return ret;
});

/**
 * Change `arr` by appling function `fn` to it's elements
 * (curried function)
 * @function
 * @param {Function} fn
 * @param {Array} arr
 * @return {Array} modified `arr`
 */
const map = curry((fn, arr) => isArray(arr) ?
    arr.map(fn) :
    pipe(toPairs,
         x => x.map(([k, v]) => [k, fn(v)]),
         fromPairs)(arr));

/**
 * Change `arr` to contain only elements for which function `fn` returns `true`
 * (curried function)
 * @function
 * @param {Function} fn
 * @param {Array} arr
 * @return {Array} filtered `arr`
 */
const filter = curry((fn, arr) => arr.filter(fn));

/**
 * Append `val` to end of `arr`
 * (curried function)
 * @function
 * @param {Any} val
 * @param {Array} arr
 * @return {Array} `arr` with appended `val`
 */
const append = curry((val, arr) => arr.concat([val]));

/**
 * Reduce `arr` values by appling function `fn`
 * (curried function)
 * @function
 * @param {Function} fn
 * @param {Any} val initial accumulator value
 * @param {Array} arr
 * @return {Any} reduced value
 */
const reduce = curry((fn, val, arr) => arr.reduce(fn, val));

/**
 * Merge two objects
 * (curried function)
 * @function
 * @param {Object} obj1
 * @param {Object} obj2
 * @return {Object} combined `obj1` and `obj2`
 */
const merge = curry((obj1, obj2) => Object.assign({}, obj1, obj2));

/**
 * Merge multiple objects
 * (curried function)
 * @function
 * @param {...Object} objs
 * @return {Object} combined `objs`
 */
const mergeAll = reduce(merge, {});

/**
 * Find element in `arr` for which function `fn` returns `true`
 * (curried function)
 * @function
 * @param {Function} fn
 * @param {Array} arr
 * @return {Any}
 */
const find = curry((fn, arr) => arr.find(fn));

/**
 * Concatenate two arrays
 * (curried function)
 * @function
 * @param {Array} arr1
 * @param {Array} arr2
 * @return {Array} concatenated `arr1` and `arr2`
 */
const concat = curry((arr1, arr2) => arr1.concat(arr2));

/**
 * Create union of two arrays using `equals` to check equality
 * (curried function)
 * @function
 * @param {Array} arr1
 * @param {Array} arr2
 * @return {Array} union of `arr1` and `arr2`
 */
const union = curry((arr1, arr2) => {
    return reduce((acc, val) => {
        if (!find(equals(val), arr1))
            acc = append(val, acc);
        return acc;
    }, arr1, arr2);
});

/**
 * Check if `arr` contains `val`
 * (curried function)
 * @function
 * @param {Any} val
 * @param {Array} arr
 * @return {Boolean}
 */
const contains = curry((val, arr) => arr.includes(val));

/**
 * Insert `val` into `arr` on index `idx`
 * (curried function)
 * @function
 * @param {Number} idx
 * @param {Any} val
 * @param {Array} arr
 * @return {Array}
 */
// TODO: Array.from(arr).splice(idx, 0, val) not working?
const insert = curry((idx, val, arr) =>
    arr.slice(0, idx).concat([val], arr.slice(idx)));

/**
 * Get array slice
 * (curried function)
 * @function
 * @param {Number} begin
 * @param {Number} end
 * @param {Array} arr
 * @return {Array}
 */
const slice = curry((begin, end, arr) => arr.slice(begin, end));

/**
 * Reverse array
 * @param  {Array} arr
 * @return {Array}
 */
function reverse(arr) {
    return Array.from(arr).reverse();
}

/**
 * Array length
 * @param  {Array} arr
 * @return {Number}
 */
function length(arr) {
    return arr.length;
}

/**
 * Create promise that resolves in `t` milliseconds
 * @param {Number} t
 * @return {Promise}
 */
function sleep(t) {
    return new Promise(resolve => {
        setTimeout(() => { resolve(); }, t);
    });
}

/**
 * Increment value
 * @param  {Number} val
 * @return {Number}
 */
function inc(val) {
    return val + 1;
}

/**
 * Decrement value
 * @param  {Number} val
 * @return {Number}
 */
function dec(val) {
    return val - 1;
}

/**
 * Logical not
 * @param  {Any} val
 * @return {Boolean}
 */
function not(val) {
    return !val;
}

/**
 * Delay function call `fn(...args)` for `t` milliseconds
 * @param {Function} fn
 * @param {Number} [t=0]
 * @param {...Any} args
 * @return {Promise}
 */
function delay(fn, t, ...args) {
    return new Promise(resolve => {
        setTimeout(() => { resolve(fn(...args)); }, t || 0);
    });
}


/***/ }),
/* 12 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "settings", function() { return settings; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Connection", function() { return Connection; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Application", function() { return Application; });
/* harmony import */ var jiff__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(13);
/* harmony import */ var jiff__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jiff__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _hat_core_util__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(11);
/* harmony import */ var _hat_core_future__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(27);
/** @module "@hat-core"/juggler
 */







/**
 * Settings
 * @property {number} settings.syncDelay sync delay [ms]
 * @property {number} settings.retryDelay retry delay [ms]
 */
const settings = {
    syncDelay: 100,
    retryDelay: 5000
};


/** Juggler client connection */
class Connection {
    /**
     * Create connection
     * @param {?string} address Juggler server address, formatted as
     *     ``ws[s]://<host>[:<port>][/<path>]``. If not provided, hostname
     *     and port obtained from ``widow.location`` are used instead, with
     *     ``ws`` as a path.
     */
    constructor(address) {
        this._localData = null;
        this._remoteData = null;
        this._onOpen = () => {};
        this._onClose = () => {};
        this._onMessage = () => {};
        this._onRemoteDataChange = () => {};
        this._delayedSyncID = null;
        this._syncedLocalData = null;

        address = address || (() => {
            const protocol = window.location.protocol == 'https:' ? 'wss' : 'ws';
            const hostname = window.location.hostname || 'localhost';
            const port = window.location.port;
            return `${protocol}://${hostname}` + (port ? `:${port}` : '') + '/ws';
        })();
        this._ws = new WebSocket(address);
        this._ws.onopen = () => this._onOpen();
        this._ws.onclose = () => {
            clearTimeout(this._delayedSyncID);
            this._onClose();
        };
        this._ws.onmessage = (evt) => {
            try {
                let msg = JSON.parse(evt.data);
                if (msg.type == 'DATA') {
                    this._remoteData = jiff__WEBPACK_IMPORTED_MODULE_0___default.a.patch(msg.payload, this._remoteData);
                    this._onRemoteDataChange(this._remoteData);
                } else if (msg.type == 'MESSAGE') {
                    this._onMessage(msg.payload);
                } else {
                    throw('unsupported message type');
                }
            } catch (e) {
                this._ws.close();
                throw e;
            }
        };
    }

    /**
     * Local data
     * @type {*}
     */
    get localData() {
        return this._localData;
    }

    /**
     * Remote data
     * @type {*}
     */
    get remoteData() {
        return this._remoteData;
    }

    /**
     * WebSocket ready state
     * @type {number}
     */
    get readyState() {
        return this._ws.readyState;
    }

    /**
     * Set on open callback
     * @type {function}
     */
    set onOpen(cb) {
        this._onOpen = cb;
    }

    /**
     * Set on close callback
     * @type {function}
     */
    set onClose(cb) {
        this._onClose = cb;
    }

    /**
     * Set on message callback
     * @type {function(*)}
     */
    set onMessage(cb) {
        this._onMessage = cb;
    }

    /**
     * Set on remote data change callback
     * @type {function(*)}
     */
    set onRemoteDataChange(cb) {
        this._onRemoteDataChange = cb;
    }

    /**
     * Close connection
     */
    close() {
        this._ws.close(1000);
    }

    /**
     * Send message
     * @param {*} msg
     */
    send(msg) {
        if (this.readyState != WebSocket.OPEN) {
            throw new Error("Connection not open");
        }
        this._ws.send(JSON.stringify({
            type: 'MESSAGE',
            payload: msg
        }));
    }

    /**
     * Set local data
     * @param {*} data
     */
    setLocalData(data) {
        if (this.readyState != WebSocket.OPEN) {
            throw new Error("Connection not open");
        }
        this._localData = data;
        if (this._delayedSyncID == null) {
            this._delayedSyncID = setTimeout(() => {
                const patch = jiff__WEBPACK_IMPORTED_MODULE_0___default.a.diff(this._syncedLocalData, this._localData);
                if (patch.length > 0) {
                    this._ws.send(JSON.stringify({
                        type: 'DATA',
                        payload: patch
                    }));
                    this._syncedLocalData = this._localData;
                }
                this._delayedSyncID = null;
            }, settings.syncDelay);
        }
    }
}


/** Juggler based application */
class Application {
    /**
     * Create application
     * @param {module:"@hat-core"/renderer.Renderer} r renderer
     * @param {?string} address juggler server address, see
     *     {@link module:"@hat-core"/juggler.Connection}
     * @param {?module:"@hat-core"/util.Path} localPath local data state path
     * @param {?module:"@hat-core"/util.Path} remotePath remote data state path
     */
    constructor(r, address, localPath, remotePath) {
        this._conn = null;
        this._onMessage = () => {};

        if (localPath != null) {
            r.addEventListener('change', () => {
                if (this._conn && this._conn.readyState == WebSocket.OPEN) {
                    this._conn.setLocalData(r.get(localPath));
                }
            });
        }

        _hat_core_util__WEBPACK_IMPORTED_MODULE_1__["delay"](async () => {
            while (true) {
                const closeFuture = _hat_core_future__WEBPACK_IMPORTED_MODULE_2__["create"]();
                this._conn = new Connection(address);
                this._conn._onOpen = () =>{
                    if (localPath != null) {
                        this._conn.setLocalData(r.get(localPath));
                    }
                };
                this._conn._onMessage = this._onMessage;
                this._conn._onRemoteDataChange = data => {
                    if (remotePath != null) r.set(remotePath, data);
                };
                this._conn._onClose = () => {
                    if (remotePath != null) r.set(remotePath, null);
                    this._conn = null;
                    closeFuture.setResult();
                };
                await closeFuture;
                await _hat_core_util__WEBPACK_IMPORTED_MODULE_1__["sleep"](settings.retryDelay);
            }
        });
    }

    /**
     * Set on message callback
     * @type {function(*)}
     */
    set onMessage(cb) {
        this._onMessage = cb;
        if (this._conn) {
            this._conn._onMessage = cb;
        }
    }

    /**
     * Send message
     * @param {*} msg
     */
    send(msg) {
        if(this._conn) {
            this._conn.send(msg);
        } else {
            throw new Error("Connection closed");
        }
    }
}


/***/ }),
/* 13 */
/***/ (function(module, exports, __webpack_require__) {

/** @license MIT License (c) copyright 2010-2014 original author or authors */
/** @author Brian Cavalier */
/** @author John Hann */

var lcs = __webpack_require__(14);
var array = __webpack_require__(15);
var patch = __webpack_require__(16);
var inverse = __webpack_require__(26);
var jsonPointer = __webpack_require__(18);
var encodeSegment = jsonPointer.encodeSegment;

exports.diff = diff;
exports.patch = patch.apply;
exports.patchInPlace = patch.applyInPlace;
exports.inverse = inverse;
exports.clone = patch.clone;

// Errors
exports.InvalidPatchOperationError = __webpack_require__(24);
exports.TestFailedError = __webpack_require__(23);
exports.PatchNotInvertibleError = __webpack_require__(25);

var isValidObject = patch.isValidObject;
var defaultHash = patch.defaultHash;

/**
 * Compute a JSON Patch representing the differences between a and b.
 * @param {object|array|string|number|null} a
 * @param {object|array|string|number|null} b
 * @param {?function|?object} options if a function, see options.hash
 * @param {?function(x:*):String|Number} options.hash used to hash array items
 *  in order to recognize identical objects, defaults to JSON.stringify
 * @param {?function(index:Number, array:Array):object} options.makeContext
 *  used to generate patch context. If not provided, context will not be generated
 * @returns {array} JSON Patch such that patch(diff(a, b), a) ~ b
 */
function diff(a, b, options) {
	return appendChanges(a, b, '', initState(options, [])).patch;
}

/**
 * Create initial diff state from the provided options
 * @param {?function|?object} options @see diff options above
 * @param {array} patch an empty or existing JSON Patch array into which
 *  the diff should generate new patch operations
 * @returns {object} initialized diff state
 */
function initState(options, patch) {
	if(typeof options === 'object') {
		return {
			patch: patch,
			hash: orElse(isFunction, options.hash, defaultHash),
			makeContext: orElse(isFunction, options.makeContext, defaultContext),
			invertible: !(options.invertible === false)
		};
	} else {
		return {
			patch: patch,
			hash: orElse(isFunction, options, defaultHash),
			makeContext: defaultContext,
			invertible: true
		};
	}
}

/**
 * Given two JSON values (object, array, number, string, etc.), find their
 * differences and append them to the diff state
 * @param {object|array|string|number|null} a
 * @param {object|array|string|number|null} b
 * @param {string} path
 * @param {object} state
 * @returns {Object} updated diff state
 */
function appendChanges(a, b, path, state) {
	if(Array.isArray(a) && Array.isArray(b)) {
		return appendArrayChanges(a, b, path, state);
	}

	if(isValidObject(a) && isValidObject(b)) {
		return appendObjectChanges(a, b, path, state);
	}

	return appendValueChanges(a, b, path, state);
}

/**
 * Given two objects, find their differences and append them to the diff state
 * @param {object} o1
 * @param {object} o2
 * @param {string} path
 * @param {object} state
 * @returns {Object} updated diff state
 */
function appendObjectChanges(o1, o2, path, state) {
	var keys = Object.keys(o2);
	var patch = state.patch;
	var i, key;

	for(i=keys.length-1; i>=0; --i) {
		key = keys[i];
		var keyPath = path + '/' + encodeSegment(key);
		if(o1[key] !== void 0) {
			appendChanges(o1[key], o2[key], keyPath, state);
		} else {
			patch.push({ op: 'add', path: keyPath, value: o2[key] });
		}
	}

	keys = Object.keys(o1);
	for(i=keys.length-1; i>=0; --i) {
		key = keys[i];
		if(o2[key] === void 0) {
			var p = path + '/' + encodeSegment(key);
			if(state.invertible) {
				patch.push({ op: 'test', path: p, value: o1[key] });
			}
			patch.push({ op: 'remove', path: p });
		}
	}

	return state;
}

/**
 * Given two arrays, find their differences and append them to the diff state
 * @param {array} a1
 * @param {array} a2
 * @param {string} path
 * @param {object} state
 * @returns {Object} updated diff state
 */
function appendArrayChanges(a1, a2, path, state) {
	var a1hash = array.map(state.hash, a1);
	var a2hash = array.map(state.hash, a2);

	var lcsMatrix = lcs.compare(a1hash, a2hash);

	return lcsToJsonPatch(a1, a2, path, state, lcsMatrix);
}

/**
 * Transform an lcsMatrix into JSON Patch operations and append
 * them to state.patch, recursing into array elements as necessary
 * @param {array} a1
 * @param {array} a2
 * @param {string} path
 * @param {object} state
 * @param {object} lcsMatrix
 * @returns {object} new state with JSON Patch operations added based
 *  on the provided lcsMatrix
 */
function lcsToJsonPatch(a1, a2, path, state, lcsMatrix) {
	var offset = 0;
	return lcs.reduce(function(state, op, i, j) {
		var last, context;
		var patch = state.patch;
		var p = path + '/' + (j + offset);

		if (op === lcs.REMOVE) {
			// Coalesce adjacent remove + add into replace
			last = patch[patch.length-1];
			context = state.makeContext(j, a1);

			if(state.invertible) {
				patch.push({ op: 'test', path: p, value: a1[j], context: context });
			}

			if(last !== void 0 && last.op === 'add' && last.path === p) {
				last.op = 'replace';
				last.context = context;
			} else {
				patch.push({ op: 'remove', path: p, context: context });
			}

			offset -= 1;

		} else if (op === lcs.ADD) {
			// See https://tools.ietf.org/html/rfc6902#section-4.1
			// May use either index===length *or* '-' to indicate appending to array
			patch.push({ op: 'add', path: p, value: a2[i],
				context: state.makeContext(j, a1)
			});

			offset += 1;

		} else {
			appendChanges(a1[j], a2[i], p, state);
		}

		return state;

	}, state, lcsMatrix);
}

/**
 * Given two number|string|null values, if they differ, append to diff state
 * @param {string|number|null} a
 * @param {string|number|null} b
 * @param {string} path
 * @param {object} state
 * @returns {object} updated diff state
 */
function appendValueChanges(a, b, path, state) {
	if(a !== b) {
		if(state.invertible) {
			state.patch.push({ op: 'test', path: path, value: a });
		}

		state.patch.push({ op: 'replace', path: path, value: b });
	}

	return state;
}

/**
 * @param {function} predicate
 * @param {*} x
 * @param {*} y
 * @returns {*} x if predicate(x) is truthy, otherwise y
 */
function orElse(predicate, x, y) {
	return predicate(x) ? x : y;
}

/**
 * Default patch context generator
 * @returns {undefined} undefined context
 */
function defaultContext() {
	return void 0;
}

/**
 * @param {*} x
 * @returns {boolean} true if x is a function, false otherwise
 */
function isFunction(x) {
	return typeof x === 'function';
}


/***/ }),
/* 14 */
/***/ (function(module, exports) {

/** @license MIT License (c) copyright 2010-2014 original author or authors */
/** @author Brian Cavalier */
/** @author John Hann */

exports.compare = compare;
exports.reduce = reduce;

var REMOVE, RIGHT, ADD, DOWN, SKIP;

exports.REMOVE = REMOVE = RIGHT = -1;
exports.ADD    = ADD    = DOWN  =  1;
exports.EQUAL  = SKIP   = 0;

/**
 * Create an lcs comparison matrix describing the differences
 * between two array-like sequences
 * @param {array} a array-like
 * @param {array} b array-like
 * @returns {object} lcs descriptor, suitable for passing to reduce()
 */
function compare(a, b) {
	var cols = a.length;
	var rows = b.length;

	var prefix = findPrefix(a, b);
	var suffix = prefix < cols && prefix < rows
		? findSuffix(a, b, prefix)
		: 0;

	var remove = suffix + prefix - 1;
	cols -= remove;
	rows -= remove;
	var matrix = createMatrix(cols, rows);

	for (var j = cols - 1; j >= 0; --j) {
		for (var i = rows - 1; i >= 0; --i) {
			matrix[i][j] = backtrack(matrix, a, b, prefix, j, i);
		}
	}

	return {
		prefix: prefix,
		matrix: matrix,
		suffix: suffix
	};
}

/**
 * Reduce a set of lcs changes previously created using compare
 * @param {function(result:*, type:number, i:number, j:number)} f
 *  reducer function, where:
 *  - result is the current reduce value,
 *  - type is the type of change: ADD, REMOVE, or SKIP
 *  - i is the index of the change location in b
 *  - j is the index of the change location in a
 * @param {*} r initial value
 * @param {object} lcs results returned by compare()
 * @returns {*} the final reduced value
 */
function reduce(f, r, lcs) {
	var i, j, k, op;

	var m = lcs.matrix;

	// Reduce shared prefix
	var l = lcs.prefix;
	for(i = 0;i < l; ++i) {
		r = f(r, SKIP, i, i);
	}

	// Reduce longest change span
	k = i;
	l = m.length;
	i = 0;
	j = 0;
	while(i < l) {
		op = m[i][j].type;
		r = f(r, op, i+k, j+k);

		switch(op) {
			case SKIP:  ++i; ++j; break;
			case RIGHT: ++j; break;
			case DOWN:  ++i; break;
		}
	}

	// Reduce shared suffix
	i += k;
	j += k;
	l = lcs.suffix;
	for(k = 0;k < l; ++k) {
		r = f(r, SKIP, i+k, j+k);
	}

	return r;
}

function findPrefix(a, b) {
	var i = 0;
	var l = Math.min(a.length, b.length);
	while(i < l && a[i] === b[i]) {
		++i;
	}
	return i;
}

function findSuffix(a, b) {
	var al = a.length - 1;
	var bl = b.length - 1;
	var l = Math.min(al, bl);
	var i = 0;
	while(i < l && a[al-i] === b[bl-i]) {
		++i;
	}
	return i;
}

function backtrack(matrix, a, b, start, j, i) {
	if (a[j+start] === b[i+start]) {
		return { value: matrix[i + 1][j + 1].value, type: SKIP };
	}
	if (matrix[i][j + 1].value < matrix[i + 1][j].value) {
		return { value: matrix[i][j + 1].value + 1, type: RIGHT };
	}

	return { value: matrix[i + 1][j].value + 1, type: DOWN };
}

function createMatrix (cols, rows) {
	var m = [], i, j, lastrow;

	// Fill the last row
	lastrow = m[rows] = [];
	for (j = 0; j<cols; ++j) {
		lastrow[j] = { value: cols - j, type: RIGHT };
	}

	// Fill the last col
	for (i = 0; i<rows; ++i) {
		m[i] = [];
		m[i][cols] = { value: rows - i, type: DOWN };
	}

	// Fill the last cell
	m[rows][cols] = { value: 0, type: SKIP };

	return m;
}


/***/ }),
/* 15 */
/***/ (function(module, exports) {

/** @license MIT License (c) copyright 2010-2014 original author or authors */
/** @author Brian Cavalier */
/** @author John Hann */

exports.cons = cons;
exports.tail = tail;
exports.map = map;

/**
 * Prepend x to a, without mutating a. Faster than a.unshift(x)
 * @param {*} x
 * @param {Array} a array-like
 * @returns {Array} new Array with x prepended
 */
function cons(x, a) {
	var l = a.length;
	var b = new Array(l+1);
	b[0] = x;
	for(var i=0; i<l; ++i) {
		b[i+1] = a[i];
	}

	return b;
}

/**
 * Create a new Array containing all elements in a, except the first.
 *  Faster than a.slice(1)
 * @param {Array} a array-like
 * @returns {Array} new Array, the equivalent of a.slice(1)
 */
function tail(a) {
	var l = a.length-1;
	var b = new Array(l);
	for(var i=0; i<l; ++i) {
		b[i] = a[i+1];
	}

	return b;
}

/**
 * Map any array-like. Faster than Array.prototype.map
 * @param {function} f
 * @param {Array} a array-like
 * @returns {Array} new Array mapped by f
 */
function map(f, a) {
	var b = new Array(a.length);
	for(var i=0; i< a.length; ++i) {
		b[i] = f(a[i]);
	}
	return b;
}

/***/ }),
/* 16 */
/***/ (function(module, exports, __webpack_require__) {

/** @license MIT License (c) copyright 2010-2014 original author or authors */
/** @author Brian Cavalier */
/** @author John Hann */

var patches = __webpack_require__(17);
var clone = __webpack_require__(20);
var InvalidPatchOperationError = __webpack_require__(24);

exports.apply = patch;
exports.applyInPlace = patchInPlace;
exports.clone = clone;
exports.isValidObject = isValidObject;
exports.defaultHash = defaultHash;

var defaultOptions = {};

/**
 * Apply the supplied JSON Patch to x
 * @param {array} changes JSON Patch
 * @param {object|array|string|number} x object/array/value to patch
 * @param {object} options
 * @param {function(index:Number, array:Array, context:object):Number} options.findContext
 *  function used adjust array indexes for smarty/fuzzy patching, for
 *  patches containing context
 * @returns {object|array|string|number} patched version of x. If x is
 *  an array or object, it will be mutated and returned. Otherwise, if
 *  x is a value, the new value will be returned.
 */
function patch(changes, x, options) {
	return patchInPlace(changes, clone(x), options);
}

function patchInPlace(changes, x, options) {
	if(!options) {
		options = defaultOptions;
	}

	// TODO: Consider throwing if changes is not an array
	if(!Array.isArray(changes)) {
		return x;
	}

	var patch, p;
	for(var i=0; i<changes.length; ++i) {
		p = changes[i];
		patch = patches[p.op];

		if(patch === void 0) {
			throw new InvalidPatchOperationError('invalid op ' + JSON.stringify(p));
		}

		x = patch.apply(x, p, options);
	}

	return x;
}

function defaultHash(x) {
	return isValidObject(x) || isArray(x) ? JSON.stringify(x) : x;
}

function isValidObject (x) {
	return x !== null && Object.prototype.toString.call(x) === '[object Object]';
}

function isArray (x) {
	return Object.prototype.toString.call(x) === '[object Array]';
}


/***/ }),
/* 17 */
/***/ (function(module, exports, __webpack_require__) {

var jsonPointer = __webpack_require__(18);
var clone = __webpack_require__(20);
var deepEquals = __webpack_require__(21);
var commutePaths = __webpack_require__(22);

var array = __webpack_require__(15);

var TestFailedError = __webpack_require__(23);
var InvalidPatchOperationError = __webpack_require__(24);
var PatchNotInvertibleError = __webpack_require__(25);

var find = jsonPointer.find;
var parseArrayIndex = jsonPointer.parseArrayIndex;

exports.test = {
	apply: applyTest,
	inverse: invertTest,
	commute: commuteTest
};

exports.add = {
	apply: applyAdd,
	inverse: invertAdd,
	commute: commuteAddOrCopy
};

exports.remove = {
	apply: applyRemove,
	inverse: invertRemove,
	commute: commuteRemove
};

exports.replace = {
	apply: applyReplace,
	inverse: invertReplace,
	commute: commuteReplace
};

exports.move = {
	apply: applyMove,
	inverse: invertMove,
	commute: commuteMove
};

exports.copy = {
	apply: applyCopy,
	inverse: notInvertible,
	commute: commuteAddOrCopy
};

/**
 * Apply a test operation to x
 * @param {object|array} x
 * @param {object} test test operation
 * @throws {TestFailedError} if the test operation fails
 */

function applyTest(x, test, options) {
	var pointer = find(x, test.path, options.findContext, test.context);
	var target = pointer.target;
	var index, value;

	if(Array.isArray(target)) {
		index = parseArrayIndex(pointer.key);
		//index = findIndex(options.findContext, index, target, test.context);
		value = target[index];
	} else {
		value = pointer.key === void 0 ? pointer.target : pointer.target[pointer.key];
	}

	if(!deepEquals(value, test.value)) {
		throw new TestFailedError('test failed ' + JSON.stringify(test));
	}

	return x;
}

/**
 * Invert the provided test and add it to the inverted patch sequence
 * @param pr
 * @param test
 * @returns {number}
 */
function invertTest(pr, test) {
	pr.push(test);
	return 1;
}

function commuteTest(test, b) {
	if(test.path === b.path && b.op === 'remove') {
		throw new TypeError('Can\'t commute test,remove -> remove,test for same path');
	}

	if(b.op === 'test' || b.op === 'replace') {
		return [b, test];
	}

	return commutePaths(test, b);
}

/**
 * Apply an add operation to x
 * @param {object|array} x
 * @param {object} change add operation
 */
function applyAdd(x, change, options) {
	var pointer = find(x, change.path, options.findContext, change.context);

	if(notFound(pointer)) {
		throw new InvalidPatchOperationError('path does not exist ' + change.path);
	}

	if(change.value === void 0) {
		throw new InvalidPatchOperationError('missing value');
	}

	var val = clone(change.value);

	// If pointer refers to whole document, replace whole document
	if(pointer.key === void 0) {
		return val;
	}

	_add(pointer, val);
	return x;
}

function _add(pointer, value) {
	var target = pointer.target;

	if(Array.isArray(target)) {
		// '-' indicates 'append' to array
		if(pointer.key === '-') {
			target.push(value);
		} else if (pointer.key > target.length) {
			throw new InvalidPatchOperationError('target of add outside of array bounds')
		} else {
			target.splice(pointer.key, 0, value);
		}
	} else if(isValidObject(target)) {
		target[pointer.key] = value;
	} else {
		throw new InvalidPatchOperationError('target of add must be an object or array ' + pointer.key);
	}
}

function invertAdd(pr, add) {
	var context = add.context;
	if(context !== void 0) {
		context = {
			before: context.before,
			after: array.cons(add.value, context.after)
		}
	}
	pr.push({ op: 'test', path: add.path, value: add.value, context: context });
	pr.push({ op: 'remove', path: add.path, context: context });
	return 1;
}

function commuteAddOrCopy(add, b) {
	if(add.path === b.path && b.op === 'remove') {
		throw new TypeError('Can\'t commute add,remove -> remove,add for same path');
	}

	return commutePaths(add, b);
}

/**
 * Apply a replace operation to x
 * @param {object|array} x
 * @param {object} change replace operation
 */
function applyReplace(x, change, options) {
	var pointer = find(x, change.path, options.findContext, change.context);

	if(notFound(pointer) || missingValue(pointer)) {
		throw new InvalidPatchOperationError('path does not exist ' + change.path);
	}

	if(change.value === void 0) {
		throw new InvalidPatchOperationError('missing value');
	}

	var value = clone(change.value);

	// If pointer refers to whole document, replace whole document
	if(pointer.key === void 0) {
		return value;
	}

	var target = pointer.target;

	if(Array.isArray(target)) {
		target[parseArrayIndex(pointer.key)] = value;
	} else {
		target[pointer.key] = value;
	}

	return x;
}

function invertReplace(pr, c, i, patch) {
	var prev = patch[i-1];
	if(prev === void 0 || prev.op !== 'test' || prev.path !== c.path) {
		throw new PatchNotInvertibleError('cannot invert replace w/o test');
	}

	var context = prev.context;
	if(context !== void 0) {
		context = {
			before: context.before,
			after: array.cons(prev.value, array.tail(context.after))
		}
	}

	pr.push({ op: 'test', path: prev.path, value: c.value });
	pr.push({ op: 'replace', path: prev.path, value: prev.value });
	return 2;
}

function commuteReplace(replace, b) {
	if(replace.path === b.path && b.op === 'remove') {
		throw new TypeError('Can\'t commute replace,remove -> remove,replace for same path');
	}

	if(b.op === 'test' || b.op === 'replace') {
		return [b, replace];
	}

	return commutePaths(replace, b);
}

/**
 * Apply a remove operation to x
 * @param {object|array} x
 * @param {object} change remove operation
 */
function applyRemove(x, change, options) {
	var pointer = find(x, change.path, options.findContext, change.context);

	// key must exist for remove
	if(notFound(pointer) || pointer.target[pointer.key] === void 0) {
		throw new InvalidPatchOperationError('path does not exist ' + change.path);
	}

	_remove(pointer);
	return x;
}

function _remove (pointer) {
	var target = pointer.target;

	var removed;
	if (Array.isArray(target)) {
		removed = target.splice(parseArrayIndex(pointer.key), 1);
		return removed[0];

	} else if (isValidObject(target)) {
		removed = target[pointer.key];
		delete target[pointer.key];
		return removed;

	} else {
		throw new InvalidPatchOperationError('target of remove must be an object or array');
	}
}

function invertRemove(pr, c, i, patch) {
	var prev = patch[i-1];
	if(prev === void 0 || prev.op !== 'test' || prev.path !== c.path) {
		throw new PatchNotInvertibleError('cannot invert remove w/o test');
	}

	var context = prev.context;
	if(context !== void 0) {
		context = {
			before: context.before,
			after: array.tail(context.after)
		}
	}

	pr.push({ op: 'add', path: prev.path, value: prev.value, context: context });
	return 2;
}

function commuteRemove(remove, b) {
	if(remove.path === b.path && b.op === 'remove') {
		return [b, remove];
	}

	return commutePaths(remove, b);
}

/**
 * Apply a move operation to x
 * @param {object|array} x
 * @param {object} change move operation
 */
function applyMove(x, change, options) {
	if(jsonPointer.contains(change.path, change.from)) {
		throw new InvalidPatchOperationError('move.from cannot be ancestor of move.path');
	}

	var pto = find(x, change.path, options.findContext, change.context);
	var pfrom = find(x, change.from, options.findContext, change.fromContext);

	_add(pto, _remove(pfrom));
	return x;
}

function invertMove(pr, c) {
	pr.push({ op: 'move',
		path: c.from, context: c.fromContext,
		from: c.path, fromContext: c.context });
	return 1;
}

function commuteMove(move, b) {
	if(move.path === b.path && b.op === 'remove') {
		throw new TypeError('Can\'t commute move,remove -> move,replace for same path');
	}

	return commutePaths(move, b);
}

/**
 * Apply a copy operation to x
 * @param {object|array} x
 * @param {object} change copy operation
 */
function applyCopy(x, change, options) {
	var pto = find(x, change.path, options.findContext, change.context);
	var pfrom = find(x, change.from, options.findContext, change.fromContext);

	if(notFound(pfrom) || missingValue(pfrom)) {
		throw new InvalidPatchOperationError('copy.from must exist');
	}

	var target = pfrom.target;
	var value;

	if(Array.isArray(target)) {
		value = target[parseArrayIndex(pfrom.key)];
	} else {
		value = target[pfrom.key];
	}

	_add(pto, clone(value));
	return x;
}

// NOTE: Copy is not invertible
// See https://github.com/cujojs/jiff/issues/9
// This needs more thought. We may have to extend/amend JSON Patch.
// At first glance, this seems like it should just be a remove.
// However, that's not correct.  It violates the involution:
// invert(invert(p)) ~= p.  For example:
// invert(copy) -> remove
// invert(remove) -> add
// thus: invert(invert(copy)) -> add (DOH! this should be copy!)

function notInvertible(_, c) {
	throw new PatchNotInvertibleError('cannot invert ' + c.op);
}

function notFound (pointer) {
	return pointer === void 0 || (pointer.target == null && pointer.key !== void 0);
}

function missingValue(pointer) {
	return pointer.key !== void 0 && pointer.target[pointer.key] === void 0;
}

/**
 * Return true if x is a non-null object
 * @param {*} x
 * @returns {boolean}
 */
function isValidObject (x) {
	return x !== null && typeof x === 'object';
}


/***/ }),
/* 18 */
/***/ (function(module, exports, __webpack_require__) {

/** @license MIT License (c) copyright 2010-2014 original author or authors */
/** @author Brian Cavalier */
/** @author John Hann */

var _parse = __webpack_require__(19);

exports.find = find;
exports.join = join;
exports.absolute = absolute;
exports.parse = parse;
exports.contains = contains;
exports.encodeSegment = encodeSegment;
exports.decodeSegment = decodeSegment;
exports.parseArrayIndex = parseArrayIndex;
exports.isValidArrayIndex = isValidArrayIndex;

// http://tools.ietf.org/html/rfc6901#page-2
var separator = '/';
var separatorRx = /\//g;
var encodedSeparator = '~1';
var encodedSeparatorRx = /~1/g;

var escapeChar = '~';
var escapeRx = /~/g;
var encodedEscape = '~0';
var encodedEscapeRx = /~0/g;

/**
 * Find the parent of the specified path in x and return a descriptor
 * containing the parent and a key.  If the parent does not exist in x,
 * return undefined, instead.
 * @param {object|array} x object or array in which to search
 * @param {string} path JSON Pointer string (encoded)
 * @param {?function(index:Number, array:Array, context:object):Number} findContext
 *  optional function used adjust array indexes for smarty/fuzzy patching, for
 *  patches containing context.  If provided, context MUST also be provided.
 * @param {?{before:Array, after:Array}} context optional patch context for
 *  findContext to use to adjust array indices.  If provided, findContext MUST
 *  also be provided.
 * @returns {{target:object|array|number|string, key:string}|undefined}
 */
function find(x, path, findContext, context) {
	if(typeof path !== 'string') {
		return;
	}

	if(path === '') {
		// whole document
		return { target: x, key: void 0 };
	}

	if(path === separator) {
		return { target: x, key: '' };
	}

	var parent = x, key;
	var hasContext = context !== void 0;

	_parse(path, function(segment) {
		// hm... this seems like it should be if(typeof x === 'undefined')
		if(x == null) {
			// Signal that we prematurely hit the end of the path hierarchy.
			parent = null;
			return false;
		}

		if(Array.isArray(x)) {
			key = hasContext
				? findIndex(findContext, parseArrayIndex(segment), x, context)
				: segment === '-' ? segment : parseArrayIndex(segment);
		} else {
			key = segment;
		}

		parent = x;
		x = x[key];
	});

	return parent === null
		? void 0
		: { target: parent, key: key };
}

function absolute(path) {
	return path[0] === separator ? path : separator + path;
}

function join(segments) {
	return segments.join(separator);
}

function parse(path) {
	var segments = [];
	_parse(path, segments.push.bind(segments));
	return segments;
}

function contains(a, b) {
	return b.indexOf(a) === 0 && b[a.length] === separator;
}

/**
 * Decode a JSON Pointer path segment
 * @see http://tools.ietf.org/html/rfc6901#page-3
 * @param {string} s encoded segment
 * @returns {string} decoded segment
 */
function decodeSegment(s) {
	// See: http://tools.ietf.org/html/rfc6901#page-3
	return s.replace(encodedSeparatorRx, separator).replace(encodedEscapeRx, escapeChar);
}

/**
 * Encode a JSON Pointer path segment
 * @see http://tools.ietf.org/html/rfc6901#page-3
 * @param {string} s decoded segment
 * @returns {string} encoded segment
 */
function encodeSegment(s) {
	return s.replace(escapeRx, encodedEscape).replace(separatorRx, encodedSeparator);
}

var arrayIndexRx = /^(0|[1-9]\d*)$/;

/**
 * Return true if s is a valid JSON Pointer array index
 * @param {String} s
 * @returns {boolean}
 */
function isValidArrayIndex(s) {
	return arrayIndexRx.test(s);
}

/**
 * Safely parse a string into a number >= 0. Does not check for decimal numbers
 * @param {string} s numeric string
 * @returns {number} number >= 0
 */
function parseArrayIndex (s) {
	if(isValidArrayIndex(s)) {
		return +s;
	}

	throw new SyntaxError('invalid array index ' + s);
}

function findIndex (findContext, start, array, context) {
	var index = start;

	if(index < 0) {
		throw new Error('array index out of bounds ' + index);
	}

	if(context !== void 0 && typeof findContext === 'function') {
		index = findContext(start, array, context);
		if(index < 0) {
			throw new Error('could not find patch context ' + context);
		}
	}

	return index;
}

/***/ }),
/* 19 */
/***/ (function(module, exports) {

/** @license MIT License (c) copyright 2010-2014 original author or authors */
/** @author Brian Cavalier */
/** @author John Hann */

module.exports = jsonPointerParse;

var parseRx = /\/|~1|~0/g;
var separator = '/';
var escapeChar = '~';
var encodedSeparator = '~1';

/**
 * Parse through an encoded JSON Pointer string, decoding each path segment
 * and passing it to an onSegment callback function.
 * @see https://tools.ietf.org/html/rfc6901#section-4
 * @param {string} path encoded JSON Pointer string
 * @param {{function(segment:string):boolean}} onSegment callback function
 * @returns {string} original path
 */
function jsonPointerParse(path, onSegment) {
	var pos, accum, matches, match;

	pos = path.charAt(0) === separator ? 1 : 0;
	accum = '';
	parseRx.lastIndex = pos;

	while(matches = parseRx.exec(path)) {

		match = matches[0];
		accum += path.slice(pos, parseRx.lastIndex - match.length);
		pos = parseRx.lastIndex;

		if(match === separator) {
			if (onSegment(accum) === false) return path;
			accum = '';
		} else {
			accum += match === encodedSeparator ? separator : escapeChar;
		}
	}

	accum += path.slice(pos);
	onSegment(accum);

	return path;
}


/***/ }),
/* 20 */
/***/ (function(module, exports) {

/** @license MIT License (c) copyright 2010-2014 original author or authors */
/** @author Brian Cavalier */
/** @author John Hann */

/**
 * Create a deep copy of x which must be a legal JSON object/array/value
 * @param {object|array|string|number|null} x object/array/value to clone
 * @returns {object|array|string|number|null} clone of x
 */
module.exports = clone;

function clone(x) {
	if(x == null || typeof x !== 'object') {
		return x;
	}

	if(Array.isArray(x)) {
		return cloneArray(x);
	}

	return cloneObject(x);
}

function cloneArray (x) {
	var l = x.length;
	var y = new Array(l);

	for (var i = 0; i < l; ++i) {
		y[i] = clone(x[i]);
	}

	return y;
}

function cloneObject (x) {
	var keys = Object.keys(x);
	var y = {};

	for (var k, i = 0, l = keys.length; i < l; ++i) {
		k = keys[i];
		y[k] = clone(x[k]);
	}

	return y;
}


/***/ }),
/* 21 */
/***/ (function(module, exports) {

module.exports = deepEquals;

/**
 * Compare 2 JSON values, or recursively compare 2 JSON objects or arrays
 * @param {object|array|string|number|boolean|null} a
 * @param {object|array|string|number|boolean|null} b
 * @returns {boolean} true iff a and b are recursively equal
 */
function deepEquals(a, b) {
	if(a === b) {
		return true;
	}

	if(Array.isArray(a) && Array.isArray(b)) {
		return compareArrays(a, b);
	}

	if(typeof a === 'object' && typeof b === 'object') {
		return compareObjects(a, b);
	}

	return false;
}

function compareArrays(a, b) {
	if(a.length !== b.length) {
		return false;
	}

	for(var i = 0; i<a.length; ++i) {
		if(!deepEquals(a[i], b[i])) {
			return false;
		}
	}

	return true;
}

function compareObjects(a, b) {
	if((a === null && b !== null) || (a !== null && b === null)) {
		return false;
	}

	var akeys = Object.keys(a);
	var bkeys = Object.keys(b);

	if(akeys.length !== bkeys.length) {
		return false;
	}

	for(var i = 0, k; i<akeys.length; ++i) {
		k = akeys[i];
		if(!(k in b && deepEquals(a[k], b[k]))) {
			return false;
		}
	}

	return true;
}

/***/ }),
/* 22 */
/***/ (function(module, exports, __webpack_require__) {

var jsonPointer = __webpack_require__(18);

/**
 * commute the patch sequence a,b to b,a
 * @param {object} a patch operation
 * @param {object} b patch operation
 */
module.exports = function commutePaths(a, b) {
	// TODO: cases for special paths: '' and '/'
	var left = jsonPointer.parse(a.path);
	var right = jsonPointer.parse(b.path);
	var prefix = getCommonPathPrefix(left, right);
	var isArray = isArrayPath(left, right, prefix.length);

	// Never mutate the originals
	var ac = copyPatch(a);
	var bc = copyPatch(b);

	if(prefix.length === 0 && !isArray) {
		// Paths share no common ancestor, simple swap
		return [bc, ac];
	}

	if(isArray) {
		return commuteArrayPaths(ac, left, bc, right);
	} else {
		return commuteTreePaths(ac, left, bc, right);
	}
};

function commuteTreePaths(a, left, b, right) {
	if(a.path === b.path) {
		throw new TypeError('cannot commute ' + a.op + ',' + b.op + ' with identical object paths');
	}
	// FIXME: Implement tree path commutation
	return [b, a];
}

/**
 * Commute two patches whose common ancestor (which may be the immediate parent)
 * is an array
 * @param a
 * @param left
 * @param b
 * @param right
 * @returns {*}
 */
function commuteArrayPaths(a, left, b, right) {
	if(left.length === right.length) {
		return commuteArraySiblings(a, left, b, right);
	}

	if (left.length > right.length) {
		// left is longer, commute by "moving" it to the right
		left = commuteArrayAncestor(b, right, a, left, -1);
		a.path = jsonPointer.absolute(jsonPointer.join(left));
	} else {
		// right is longer, commute by "moving" it to the left
		right = commuteArrayAncestor(a, left, b, right, 1);
		b.path = jsonPointer.absolute(jsonPointer.join(right));
	}

	return [b, a];
}

function isArrayPath(left, right, index) {
	return jsonPointer.isValidArrayIndex(left[index])
		&& jsonPointer.isValidArrayIndex(right[index]);
}

/**
 * Commute two patches referring to items in the same array
 * @param l
 * @param lpath
 * @param r
 * @param rpath
 * @returns {*[]}
 */
function commuteArraySiblings(l, lpath, r, rpath) {

	var target = lpath.length-1;
	var lindex = +lpath[target];
	var rindex = +rpath[target];

	var commuted;

	if(lindex < rindex) {
		// Adjust right path
		if(l.op === 'add' || l.op === 'copy') {
			commuted = rpath.slice();
			commuted[target] = Math.max(0, rindex - 1);
			r.path = jsonPointer.absolute(jsonPointer.join(commuted));
		} else if(l.op === 'remove') {
			commuted = rpath.slice();
			commuted[target] = rindex + 1;
			r.path = jsonPointer.absolute(jsonPointer.join(commuted));
		}
	} else if(r.op === 'add' || r.op === 'copy') {
		// Adjust left path
		commuted = lpath.slice();
		commuted[target] = lindex + 1;
		l.path = jsonPointer.absolute(jsonPointer.join(commuted));
	} else if (lindex > rindex && r.op === 'remove') {
		// Adjust left path only if remove was at a (strictly) lower index
		commuted = lpath.slice();
		commuted[target] = Math.max(0, lindex - 1);
		l.path = jsonPointer.absolute(jsonPointer.join(commuted));
	}

	return [r, l];
}

/**
 * Commute two patches with a common array ancestor
 * @param l
 * @param lpath
 * @param r
 * @param rpath
 * @param direction
 * @returns {*}
 */
function commuteArrayAncestor(l, lpath, r, rpath, direction) {
	// rpath is longer or same length

	var target = lpath.length-1;
	var lindex = +lpath[target];
	var rindex = +rpath[target];

	// Copy rpath, then adjust its array index
	var rc = rpath.slice();

	if(lindex > rindex) {
		return rc;
	}

	if(l.op === 'add' || l.op === 'copy') {
		rc[target] = Math.max(0, rindex - direction);
	} else if(l.op === 'remove') {
		rc[target] = Math.max(0, rindex + direction);
	}

	return rc;
}

function getCommonPathPrefix(p1, p2) {
	var p1l = p1.length;
	var p2l = p2.length;
	if(p1l === 0 || p2l === 0 || (p1l < 2 && p2l < 2)) {
		return [];
	}

	// If paths are same length, the last segment cannot be part
	// of a common prefix.  If not the same length, the prefix cannot
	// be longer than the shorter path.
	var l = p1l === p2l
		? p1l - 1
		: Math.min(p1l, p2l);

	var i = 0;
	while(i < l && p1[i] === p2[i]) {
		++i
	}

	return p1.slice(0, i);
}

function copyPatch(p) {
	if(p.op === 'remove') {
		return { op: p.op, path: p.path };
	}

	if(p.op === 'copy' || p.op === 'move') {
		return { op: p.op, path: p.path, from: p.from };
	}

	// test, add, replace
	return { op: p.op, path: p.path, value: p.value };
}

/***/ }),
/* 23 */
/***/ (function(module, exports) {

module.exports = TestFailedError;

function TestFailedError(message) {
	Error.call(this);
	this.name = this.constructor.name;
	this.message = message;
	if(typeof Error.captureStackTrace === 'function') {
		Error.captureStackTrace(this, this.constructor);
	}
}

TestFailedError.prototype = Object.create(Error.prototype);
TestFailedError.prototype.constructor = TestFailedError;

/***/ }),
/* 24 */
/***/ (function(module, exports) {

module.exports = InvalidPatchOperationError;

function InvalidPatchOperationError(message) {
	Error.call(this);
	this.name = this.constructor.name;
	this.message = message;
	if(typeof Error.captureStackTrace === 'function') {
		Error.captureStackTrace(this, this.constructor);
	}
}

InvalidPatchOperationError.prototype = Object.create(Error.prototype);
InvalidPatchOperationError.prototype.constructor = InvalidPatchOperationError;

/***/ }),
/* 25 */
/***/ (function(module, exports) {

module.exports = PatchNotInvertibleError;

function PatchNotInvertibleError(message) {
	Error.call(this);
	this.name = this.constructor.name;
	this.message = message;
	if(typeof Error.captureStackTrace === 'function') {
		Error.captureStackTrace(this, this.constructor);
	}
}

PatchNotInvertibleError.prototype = Object.create(Error.prototype);
PatchNotInvertibleError.prototype.constructor = PatchNotInvertibleError;

/***/ }),
/* 26 */
/***/ (function(module, exports, __webpack_require__) {

var patches = __webpack_require__(17);

module.exports = function inverse(p) {
	var pr = [];
	var i, skip;
	for(i = p.length-1; i>= 0; i -= skip) {
		skip = invertOp(pr, p[i], i, p);
	}

	return pr;
};

function invertOp(patch, c, i, context) {
	var op = patches[c.op];
	return op !== void 0 && typeof op.inverse === 'function'
		? op.inverse(patch, c, i, context)
		: 1;
}


/***/ }),
/* 27 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "create", function() { return create; });
/** @module "@hat-core"/future
 */


function create() {
    let data = {
        done: false,
        error: false,
        result: undefined,
        resolve: null,
        reject: null
    };
    let future = new Promise((resolve, reject) => {
        data.resolve = resolve;
        data.reject = reject;
        if (data.error) {
            reject(data.result);
        } else if (data.done) {
            resolve(data.resolve);
        }
    });
    future.done = () => data.done;
    future.result = () => {
        if (!data.done)
            throw 'Future is not done';
        if (data.error)
            throw data.error;
        return data.result;
    };
    future.setResult = result => {
        if (data.done)
            throw 'Result already set';
        data.result = result;
        data.done = true;
        if (data.resolve)
            data.resolve(data.result);
    };
    future.setError = error => {
        if (data.done)
            throw 'Result already set';
        data.error = true;
        data.result = error;
        data.done = true;
        if (data.reject)
            data.reject(error);
    };
    return future;
}


/***/ }),
/* 28 */
/***/ (function(module, exports, __webpack_require__) {

var api = __webpack_require__(29);
            var content = __webpack_require__(30);

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.i, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);

var exported = content.locals ? content.locals : {};



module.exports = exported;

/***/ }),
/* 29 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var isOldIE = function isOldIE() {
  var memo;
  return function memorize() {
    if (typeof memo === 'undefined') {
      // Test for IE <= 9 as proposed by Browserhacks
      // @see http://browserhacks.com/#hack-e71d8692f65334173fee715c222cb805
      // Tests for existence of standard globals is to allow style-loader
      // to operate correctly into non-standard environments
      // @see https://github.com/webpack-contrib/style-loader/issues/177
      memo = Boolean(window && document && document.all && !window.atob);
    }

    return memo;
  };
}();

var getTarget = function getTarget() {
  var memo = {};
  return function memorize(target) {
    if (typeof memo[target] === 'undefined') {
      var styleTarget = document.querySelector(target); // Special case to return head of iframe instead of iframe itself

      if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
        try {
          // This will throw an exception if access to iframe is blocked
          // due to cross-origin restrictions
          styleTarget = styleTarget.contentDocument.head;
        } catch (e) {
          // istanbul ignore next
          styleTarget = null;
        }
      }

      memo[target] = styleTarget;
    }

    return memo[target];
  };
}();

var stylesInDom = [];

function getIndexByIdentifier(identifier) {
  var result = -1;

  for (var i = 0; i < stylesInDom.length; i++) {
    if (stylesInDom[i].identifier === identifier) {
      result = i;
      break;
    }
  }

  return result;
}

function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];

  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var index = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3]
    };

    if (index !== -1) {
      stylesInDom[index].references++;
      stylesInDom[index].updater(obj);
    } else {
      stylesInDom.push({
        identifier: identifier,
        updater: addStyle(obj, options),
        references: 1
      });
    }

    identifiers.push(identifier);
  }

  return identifiers;
}

function insertStyleElement(options) {
  var style = document.createElement('style');
  var attributes = options.attributes || {};

  if (typeof attributes.nonce === 'undefined') {
    var nonce =  true ? __webpack_require__.nc : undefined;

    if (nonce) {
      attributes.nonce = nonce;
    }
  }

  Object.keys(attributes).forEach(function (key) {
    style.setAttribute(key, attributes[key]);
  });

  if (typeof options.insert === 'function') {
    options.insert(style);
  } else {
    var target = getTarget(options.insert || 'head');

    if (!target) {
      throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
    }

    target.appendChild(style);
  }

  return style;
}

function removeStyleElement(style) {
  // istanbul ignore if
  if (style.parentNode === null) {
    return false;
  }

  style.parentNode.removeChild(style);
}
/* istanbul ignore next  */


var replaceText = function replaceText() {
  var textStore = [];
  return function replace(index, replacement) {
    textStore[index] = replacement;
    return textStore.filter(Boolean).join('\n');
  };
}();

function applyToSingletonTag(style, index, remove, obj) {
  var css = remove ? '' : obj.media ? "@media ".concat(obj.media, " {").concat(obj.css, "}") : obj.css; // For old IE

  /* istanbul ignore if  */

  if (style.styleSheet) {
    style.styleSheet.cssText = replaceText(index, css);
  } else {
    var cssNode = document.createTextNode(css);
    var childNodes = style.childNodes;

    if (childNodes[index]) {
      style.removeChild(childNodes[index]);
    }

    if (childNodes.length) {
      style.insertBefore(cssNode, childNodes[index]);
    } else {
      style.appendChild(cssNode);
    }
  }
}

function applyToTag(style, options, obj) {
  var css = obj.css;
  var media = obj.media;
  var sourceMap = obj.sourceMap;

  if (media) {
    style.setAttribute('media', media);
  } else {
    style.removeAttribute('media');
  }

  if (sourceMap && btoa) {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  } // For old IE

  /* istanbul ignore if  */


  if (style.styleSheet) {
    style.styleSheet.cssText = css;
  } else {
    while (style.firstChild) {
      style.removeChild(style.firstChild);
    }

    style.appendChild(document.createTextNode(css));
  }
}

var singleton = null;
var singletonCounter = 0;

function addStyle(obj, options) {
  var style;
  var update;
  var remove;

  if (options.singleton) {
    var styleIndex = singletonCounter++;
    style = singleton || (singleton = insertStyleElement(options));
    update = applyToSingletonTag.bind(null, style, styleIndex, false);
    remove = applyToSingletonTag.bind(null, style, styleIndex, true);
  } else {
    style = insertStyleElement(options);
    update = applyToTag.bind(null, style, options);

    remove = function remove() {
      removeStyleElement(style);
    };
  }

  update(obj);
  return function updateStyle(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap) {
        return;
      }

      update(obj = newObj);
    } else {
      remove();
    }
  };
}

module.exports = function (list, options) {
  options = options || {}; // Force single-tag solution on IE6-9, which has a hard limit on the # of <style>
  // tags it will allow on a page

  if (!options.singleton && typeof options.singleton !== 'boolean') {
    options.singleton = isOldIE();
  }

  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];

    if (Object.prototype.toString.call(newList) !== '[object Array]') {
      return;
    }

    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDom[index].references--;
    }

    var newLastIdentifiers = modulesToDom(newList, options);

    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];

      var _index = getIndexByIdentifier(_identifier);

      if (stylesInDom[_index].references === 0) {
        stylesInDom[_index].updater();

        stylesInDom.splice(_index, 1);
      }
    }

    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),
/* 30 */
/***/ (function(module, exports, __webpack_require__) {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(31);
var ___CSS_LOADER_GET_URL_IMPORT___ = __webpack_require__(32);
var ___CSS_LOADER_URL_IMPORT_0___ = __webpack_require__(33);
var ___CSS_LOADER_URL_IMPORT_1___ = __webpack_require__(34);
var ___CSS_LOADER_URL_IMPORT_2___ = __webpack_require__(35);
var ___CSS_LOADER_URL_IMPORT_3___ = __webpack_require__(36);
var ___CSS_LOADER_URL_IMPORT_4___ = __webpack_require__(37);
var ___CSS_LOADER_URL_IMPORT_5___ = __webpack_require__(38);
var ___CSS_LOADER_URL_IMPORT_6___ = __webpack_require__(39);
var ___CSS_LOADER_URL_IMPORT_7___ = __webpack_require__(40);
var ___CSS_LOADER_URL_IMPORT_8___ = __webpack_require__(41);
var ___CSS_LOADER_URL_IMPORT_9___ = __webpack_require__(42);
var ___CSS_LOADER_URL_IMPORT_10___ = __webpack_require__(43);
var ___CSS_LOADER_URL_IMPORT_11___ = __webpack_require__(44);
var ___CSS_LOADER_URL_IMPORT_12___ = __webpack_require__(45);
exports = ___CSS_LOADER_API_IMPORT___(false);
var ___CSS_LOADER_URL_REPLACEMENT_0___ = ___CSS_LOADER_GET_URL_IMPORT___(___CSS_LOADER_URL_IMPORT_0___);
var ___CSS_LOADER_URL_REPLACEMENT_1___ = ___CSS_LOADER_GET_URL_IMPORT___(___CSS_LOADER_URL_IMPORT_1___);
var ___CSS_LOADER_URL_REPLACEMENT_2___ = ___CSS_LOADER_GET_URL_IMPORT___(___CSS_LOADER_URL_IMPORT_2___);
var ___CSS_LOADER_URL_REPLACEMENT_3___ = ___CSS_LOADER_GET_URL_IMPORT___(___CSS_LOADER_URL_IMPORT_3___);
var ___CSS_LOADER_URL_REPLACEMENT_4___ = ___CSS_LOADER_GET_URL_IMPORT___(___CSS_LOADER_URL_IMPORT_4___);
var ___CSS_LOADER_URL_REPLACEMENT_5___ = ___CSS_LOADER_GET_URL_IMPORT___(___CSS_LOADER_URL_IMPORT_5___);
var ___CSS_LOADER_URL_REPLACEMENT_6___ = ___CSS_LOADER_GET_URL_IMPORT___(___CSS_LOADER_URL_IMPORT_6___);
var ___CSS_LOADER_URL_REPLACEMENT_7___ = ___CSS_LOADER_GET_URL_IMPORT___(___CSS_LOADER_URL_IMPORT_7___);
var ___CSS_LOADER_URL_REPLACEMENT_8___ = ___CSS_LOADER_GET_URL_IMPORT___(___CSS_LOADER_URL_IMPORT_8___);
var ___CSS_LOADER_URL_REPLACEMENT_9___ = ___CSS_LOADER_GET_URL_IMPORT___(___CSS_LOADER_URL_IMPORT_9___);
var ___CSS_LOADER_URL_REPLACEMENT_10___ = ___CSS_LOADER_GET_URL_IMPORT___(___CSS_LOADER_URL_IMPORT_10___);
var ___CSS_LOADER_URL_REPLACEMENT_11___ = ___CSS_LOADER_GET_URL_IMPORT___(___CSS_LOADER_URL_IMPORT_11___);
var ___CSS_LOADER_URL_REPLACEMENT_12___ = ___CSS_LOADER_GET_URL_IMPORT___(___CSS_LOADER_URL_IMPORT_12___);
// Module
exports.push([module.i, "/*! normalize.css v8.0.1 | MIT License | github.com/necolas/normalize.css */\n/* Document\n   ========================================================================== */\n/**\n * 1. Correct the line height in all browsers.\n * 2. Prevent adjustments of font size after orientation changes in iOS.\n */\nhtml {\n  line-height: 1.15;\n  /* 1 */\n  -webkit-text-size-adjust: 100%;\n  /* 2 */ }\n\n/* Sections\n   ========================================================================== */\n/**\n * Remove the margin in all browsers.\n */\nbody {\n  margin: 0; }\n\n/**\n * Render the `main` element consistently in IE.\n */\nmain {\n  display: block; }\n\n/**\n * Correct the font size and margin on `h1` elements within `section` and\n * `article` contexts in Chrome, Firefox, and Safari.\n */\nh1 {\n  font-size: 2em;\n  margin: 0.67em 0; }\n\n/* Grouping content\n   ========================================================================== */\n/**\n * 1. Add the correct box sizing in Firefox.\n * 2. Show the overflow in Edge and IE.\n */\nhr {\n  box-sizing: content-box;\n  /* 1 */\n  height: 0;\n  /* 1 */\n  overflow: visible;\n  /* 2 */ }\n\n/**\n * 1. Correct the inheritance and scaling of font size in all browsers.\n * 2. Correct the odd `em` font sizing in all browsers.\n */\npre {\n  font-family: monospace, monospace;\n  /* 1 */\n  font-size: 1em;\n  /* 2 */ }\n\n/* Text-level semantics\n   ========================================================================== */\n/**\n * Remove the gray background on active links in IE 10.\n */\na {\n  background-color: transparent; }\n\n/**\n * 1. Remove the bottom border in Chrome 57-\n * 2. Add the correct text decoration in Chrome, Edge, IE, Opera, and Safari.\n */\nabbr[title] {\n  border-bottom: none;\n  /* 1 */\n  text-decoration: underline;\n  /* 2 */\n  text-decoration: underline dotted;\n  /* 2 */ }\n\n/**\n * Add the correct font weight in Chrome, Edge, and Safari.\n */\nb,\nstrong {\n  font-weight: bolder; }\n\n/**\n * 1. Correct the inheritance and scaling of font size in all browsers.\n * 2. Correct the odd `em` font sizing in all browsers.\n */\ncode,\nkbd,\nsamp {\n  font-family: monospace, monospace;\n  /* 1 */\n  font-size: 1em;\n  /* 2 */ }\n\n/**\n * Add the correct font size in all browsers.\n */\nsmall {\n  font-size: 80%; }\n\n/**\n * Prevent `sub` and `sup` elements from affecting the line height in\n * all browsers.\n */\nsub,\nsup {\n  font-size: 75%;\n  line-height: 0;\n  position: relative;\n  vertical-align: baseline; }\n\nsub {\n  bottom: -0.25em; }\n\nsup {\n  top: -0.5em; }\n\n/* Embedded content\n   ========================================================================== */\n/**\n * Remove the border on images inside links in IE 10.\n */\nimg {\n  border-style: none; }\n\n/* Forms\n   ========================================================================== */\n/**\n * 1. Change the font styles in all browsers.\n * 2. Remove the margin in Firefox and Safari.\n */\nbutton,\ninput,\noptgroup,\nselect,\ntextarea {\n  font-family: inherit;\n  /* 1 */\n  font-size: 100%;\n  /* 1 */\n  line-height: 1.15;\n  /* 1 */\n  margin: 0;\n  /* 2 */ }\n\n/**\n * Show the overflow in IE.\n * 1. Show the overflow in Edge.\n */\nbutton,\ninput {\n  /* 1 */\n  overflow: visible; }\n\n/**\n * Remove the inheritance of text transform in Edge, Firefox, and IE.\n * 1. Remove the inheritance of text transform in Firefox.\n */\nbutton,\nselect {\n  /* 1 */\n  text-transform: none; }\n\n/**\n * Correct the inability to style clickable types in iOS and Safari.\n */\nbutton,\n[type=\"button\"],\n[type=\"reset\"],\n[type=\"submit\"] {\n  -webkit-appearance: button; }\n\n/**\n * Remove the inner border and padding in Firefox.\n */\nbutton::-moz-focus-inner,\n[type=\"button\"]::-moz-focus-inner,\n[type=\"reset\"]::-moz-focus-inner,\n[type=\"submit\"]::-moz-focus-inner {\n  border-style: none;\n  padding: 0; }\n\n/**\n * Restore the focus styles unset by the previous rule.\n */\nbutton:-moz-focusring,\n[type=\"button\"]:-moz-focusring,\n[type=\"reset\"]:-moz-focusring,\n[type=\"submit\"]:-moz-focusring {\n  outline: 1px dotted ButtonText; }\n\n/**\n * Correct the padding in Firefox.\n */\nfieldset {\n  padding: 0.35em 0.75em 0.625em; }\n\n/**\n * 1. Correct the text wrapping in Edge and IE.\n * 2. Correct the color inheritance from `fieldset` elements in IE.\n * 3. Remove the padding so developers are not caught out when they zero out\n *    `fieldset` elements in all browsers.\n */\nlegend {\n  box-sizing: border-box;\n  /* 1 */\n  color: inherit;\n  /* 2 */\n  display: table;\n  /* 1 */\n  max-width: 100%;\n  /* 1 */\n  padding: 0;\n  /* 3 */\n  white-space: normal;\n  /* 1 */ }\n\n/**\n * Add the correct vertical alignment in Chrome, Firefox, and Opera.\n */\nprogress {\n  vertical-align: baseline; }\n\n/**\n * Remove the default vertical scrollbar in IE 10+.\n */\ntextarea {\n  overflow: auto; }\n\n/**\n * 1. Add the correct box sizing in IE 10.\n * 2. Remove the padding in IE 10.\n */\n[type=\"checkbox\"],\n[type=\"radio\"] {\n  box-sizing: border-box;\n  /* 1 */\n  padding: 0;\n  /* 2 */ }\n\n/**\n * Correct the cursor style of increment and decrement buttons in Chrome.\n */\n[type=\"number\"]::-webkit-inner-spin-button,\n[type=\"number\"]::-webkit-outer-spin-button {\n  height: auto; }\n\n/**\n * 1. Correct the odd appearance in Chrome and Safari.\n * 2. Correct the outline style in Safari.\n */\n[type=\"search\"] {\n  -webkit-appearance: textfield;\n  /* 1 */\n  outline-offset: -2px;\n  /* 2 */ }\n\n/**\n * Remove the inner padding in Chrome and Safari on macOS.\n */\n[type=\"search\"]::-webkit-search-decoration {\n  -webkit-appearance: none; }\n\n/**\n * 1. Correct the inability to style clickable types in iOS and Safari.\n * 2. Change font properties to `inherit` in Safari.\n */\n::-webkit-file-upload-button {\n  -webkit-appearance: button;\n  /* 1 */\n  font: inherit;\n  /* 2 */ }\n\n/* Interactive\n   ========================================================================== */\n/*\n * Add the correct display in Edge, IE 10+, and Firefox.\n */\ndetails {\n  display: block; }\n\n/*\n * Add the correct display in all browsers.\n */\nsummary {\n  display: list-item; }\n\n/* Misc\n   ========================================================================== */\n/**\n * Add the correct display in IE 10+.\n */\ntemplate {\n  display: none; }\n\n/**\n * Add the correct display in IE 10.\n */\n[hidden] {\n  display: none; }\n\ntable.grid, .orchestrator table {\n  table-layout: fixed;\n  border-spacing: 0px;\n  width: 100%;\n  border: 1px solid #bdbdbd; }\n  table.grid td:not(:last-child), .orchestrator table td:not(:last-child) {\n    border-right: 1px solid #e0e0e0; }\n  table.grid thead tr, .orchestrator table thead tr, table.grid tfoot tr, .orchestrator table tfoot tr {\n    background-color: #eeeeee; }\n  table.grid td, .orchestrator table td, table.grid th, .orchestrator table th {\n    padding: 4px;\n    overflow: hidden;\n    text-overflow: ellipsis; }\n  table.grid tbody td, .orchestrator table tbody td, table.grid tfoot td, .orchestrator table tfoot td {\n    border-top: 1px solid #bdbdbd; }\n  table.grid input, .orchestrator table input {\n    width: 100%; }\n  table.grid input[type=text], .orchestrator table input[type=text] {\n    position: relative;\n    border: 1px; }\n  table.grid tfoot td > div, .orchestrator table tfoot td > div {\n    display: flex; }\n    table.grid tfoot td > div > .spacer, .orchestrator table tfoot td > div > .spacer {\n      flex-grow: 1; }\n  table.grid .invalid, .orchestrator table .invalid {\n    background-color: rgba(255, 0, 0, 0.2); }\n\n@font-face {\n  font-family: \"Roboto\";\n  src: url(" + ___CSS_LOADER_URL_REPLACEMENT_0___ + ") format(\"woff2\");\n  font-weight: 900;\n  font-style: normal; }\n\n@font-face {\n  font-family: \"Roboto\";\n  src: url(" + ___CSS_LOADER_URL_REPLACEMENT_1___ + ") format(\"woff2\");\n  font-weight: 900;\n  font-style: italic; }\n\n@font-face {\n  font-family: \"Roboto\";\n  src: url(" + ___CSS_LOADER_URL_REPLACEMENT_2___ + ") format(\"woff2\");\n  font-weight: 700;\n  font-style: normal; }\n\n@font-face {\n  font-family: \"Roboto\";\n  src: url(" + ___CSS_LOADER_URL_REPLACEMENT_3___ + ") format(\"woff2\");\n  font-weight: 700;\n  font-style: italic; }\n\n@font-face {\n  font-family: \"Roboto\";\n  src: url(" + ___CSS_LOADER_URL_REPLACEMENT_4___ + ") format(\"woff2\");\n  font-weight: 500;\n  font-style: normal; }\n\n@font-face {\n  font-family: \"Roboto\";\n  src: url(" + ___CSS_LOADER_URL_REPLACEMENT_5___ + ") format(\"woff2\");\n  font-weight: 500;\n  font-style: italic; }\n\n@font-face {\n  font-family: \"Roboto\";\n  src: url(" + ___CSS_LOADER_URL_REPLACEMENT_6___ + ") format(\"woff2\");\n  font-weight: 400;\n  font-style: normal; }\n\n@font-face {\n  font-family: \"Roboto\";\n  src: url(" + ___CSS_LOADER_URL_REPLACEMENT_7___ + ") format(\"woff2\");\n  font-weight: 400;\n  font-style: italic; }\n\n@font-face {\n  font-family: \"Roboto\";\n  src: url(" + ___CSS_LOADER_URL_REPLACEMENT_8___ + ") format(\"woff2\");\n  font-weight: 300;\n  font-style: normal; }\n\n@font-face {\n  font-family: \"Roboto\";\n  src: url(" + ___CSS_LOADER_URL_REPLACEMENT_9___ + ") format(\"woff2\");\n  font-weight: 300;\n  font-style: italic; }\n\n@font-face {\n  font-family: \"Roboto\";\n  src: url(" + ___CSS_LOADER_URL_REPLACEMENT_10___ + ") format(\"woff2\");\n  font-weight: 100;\n  font-style: normal; }\n\n@font-face {\n  font-family: \"Roboto\";\n  src: url(" + ___CSS_LOADER_URL_REPLACEMENT_11___ + ") format(\"woff2\");\n  font-weight: 100;\n  font-style: italic; }\n\n@font-face {\n  font-family: \"FontAwesome\";\n  src: url(" + ___CSS_LOADER_URL_REPLACEMENT_12___ + ") format(\"woff2\");\n  font-weight: normal;\n  font-style: normal; }\n\n.fa {\n  display: inline-block;\n  font: normal normal normal 14px/1 FontAwesome;\n  font-size: inherit;\n  text-rendering: auto;\n  -webkit-font-smoothing: antialiased;\n  -moz-osx-font-smoothing: grayscale; }\n\n/* makes the font 33% larger relative to the icon container */\n.fa-lg {\n  font-size: 1.33333333em;\n  line-height: 0.75em;\n  vertical-align: -15%; }\n\n.fa-2x {\n  font-size: 2em; }\n\n.fa-3x {\n  font-size: 3em; }\n\n.fa-4x {\n  font-size: 4em; }\n\n.fa-5x {\n  font-size: 5em; }\n\n.fa-fw {\n  width: 1.28571429em;\n  text-align: center; }\n\n.fa-ul {\n  padding-left: 0;\n  margin-left: 2.14285714em;\n  list-style-type: none; }\n\n.fa-ul > li {\n  position: relative; }\n\n.fa-li {\n  position: absolute;\n  left: -2.14285714em;\n  width: 2.14285714em;\n  top: 0.14285714em;\n  text-align: center; }\n\n.fa-li.fa-lg {\n  left: -1.85714286em; }\n\n.fa-border {\n  padding: .2em .25em .15em;\n  border: solid 0.08em #eeeeee;\n  border-radius: .1em; }\n\n.fa-pull-left {\n  float: left; }\n\n.fa-pull-right {\n  float: right; }\n\n.fa.fa-pull-left {\n  margin-right: .3em; }\n\n.fa.fa-pull-right {\n  margin-left: .3em; }\n\n/* Deprecated as of 4.4.0 */\n.pull-right {\n  float: right; }\n\n.pull-left {\n  float: left; }\n\n.fa.pull-left {\n  margin-right: .3em; }\n\n.fa.pull-right {\n  margin-left: .3em; }\n\n.fa-spin {\n  -webkit-animation: fa-spin 2s infinite linear;\n  animation: fa-spin 2s infinite linear; }\n\n.fa-pulse {\n  -webkit-animation: fa-spin 1s infinite steps(8);\n  animation: fa-spin 1s infinite steps(8); }\n\n@-webkit-keyframes fa-spin {\n  0% {\n    -webkit-transform: rotate(0deg);\n    transform: rotate(0deg); }\n  100% {\n    -webkit-transform: rotate(359deg);\n    transform: rotate(359deg); } }\n\n@keyframes fa-spin {\n  0% {\n    -webkit-transform: rotate(0deg);\n    transform: rotate(0deg); }\n  100% {\n    -webkit-transform: rotate(359deg);\n    transform: rotate(359deg); } }\n\n.fa-rotate-90 {\n  -ms-filter: \"progid:DXImageTransform.Microsoft.BasicImage(rotation=1)\";\n  -webkit-transform: rotate(90deg);\n  -ms-transform: rotate(90deg);\n  transform: rotate(90deg); }\n\n.fa-rotate-180 {\n  -ms-filter: \"progid:DXImageTransform.Microsoft.BasicImage(rotation=2)\";\n  -webkit-transform: rotate(180deg);\n  -ms-transform: rotate(180deg);\n  transform: rotate(180deg); }\n\n.fa-rotate-270 {\n  -ms-filter: \"progid:DXImageTransform.Microsoft.BasicImage(rotation=3)\";\n  -webkit-transform: rotate(270deg);\n  -ms-transform: rotate(270deg);\n  transform: rotate(270deg); }\n\n.fa-flip-horizontal {\n  -ms-filter: \"progid:DXImageTransform.Microsoft.BasicImage(rotation=0, mirror=1)\";\n  -webkit-transform: scale(-1, 1);\n  -ms-transform: scale(-1, 1);\n  transform: scale(-1, 1); }\n\n.fa-flip-vertical {\n  -ms-filter: \"progid:DXImageTransform.Microsoft.BasicImage(rotation=2, mirror=1)\";\n  -webkit-transform: scale(1, -1);\n  -ms-transform: scale(1, -1);\n  transform: scale(1, -1); }\n\n:root .fa-rotate-90,\n:root .fa-rotate-180,\n:root .fa-rotate-270,\n:root .fa-flip-horizontal,\n:root .fa-flip-vertical {\n  filter: none; }\n\n.fa-stack {\n  position: relative;\n  display: inline-block;\n  width: 2em;\n  height: 2em;\n  line-height: 2em;\n  vertical-align: middle; }\n\n.fa-stack-1x,\n.fa-stack-2x {\n  position: absolute;\n  left: 0;\n  width: 100%;\n  text-align: center; }\n\n.fa-stack-1x {\n  line-height: inherit; }\n\n.fa-stack-2x {\n  font-size: 2em; }\n\n.fa-inverse {\n  color: #ffffff; }\n\n/* Font Awesome uses the Unicode Private Use Area (PUA) to ensure screen\n   readers do not read off random characters that represent icons */\n.fa-glass:before {\n  content: \"\\f000\"; }\n\n.fa-music:before {\n  content: \"\\f001\"; }\n\n.fa-search:before {\n  content: \"\\f002\"; }\n\n.fa-envelope-o:before {\n  content: \"\\f003\"; }\n\n.fa-heart:before {\n  content: \"\\f004\"; }\n\n.fa-star:before {\n  content: \"\\f005\"; }\n\n.fa-star-o:before {\n  content: \"\\f006\"; }\n\n.fa-user:before {\n  content: \"\\f007\"; }\n\n.fa-film:before {\n  content: \"\\f008\"; }\n\n.fa-th-large:before {\n  content: \"\\f009\"; }\n\n.fa-th:before {\n  content: \"\\f00a\"; }\n\n.fa-th-list:before {\n  content: \"\\f00b\"; }\n\n.fa-check:before {\n  content: \"\\f00c\"; }\n\n.fa-remove:before,\n.fa-close:before,\n.fa-times:before {\n  content: \"\\f00d\"; }\n\n.fa-search-plus:before {\n  content: \"\\f00e\"; }\n\n.fa-search-minus:before {\n  content: \"\\f010\"; }\n\n.fa-power-off:before {\n  content: \"\\f011\"; }\n\n.fa-signal:before {\n  content: \"\\f012\"; }\n\n.fa-gear:before,\n.fa-cog:before {\n  content: \"\\f013\"; }\n\n.fa-trash-o:before {\n  content: \"\\f014\"; }\n\n.fa-home:before {\n  content: \"\\f015\"; }\n\n.fa-file-o:before {\n  content: \"\\f016\"; }\n\n.fa-clock-o:before {\n  content: \"\\f017\"; }\n\n.fa-road:before {\n  content: \"\\f018\"; }\n\n.fa-download:before {\n  content: \"\\f019\"; }\n\n.fa-arrow-circle-o-down:before {\n  content: \"\\f01a\"; }\n\n.fa-arrow-circle-o-up:before {\n  content: \"\\f01b\"; }\n\n.fa-inbox:before {\n  content: \"\\f01c\"; }\n\n.fa-play-circle-o:before {\n  content: \"\\f01d\"; }\n\n.fa-rotate-right:before,\n.fa-repeat:before {\n  content: \"\\f01e\"; }\n\n.fa-refresh:before {\n  content: \"\\f021\"; }\n\n.fa-list-alt:before {\n  content: \"\\f022\"; }\n\n.fa-lock:before {\n  content: \"\\f023\"; }\n\n.fa-flag:before {\n  content: \"\\f024\"; }\n\n.fa-headphones:before {\n  content: \"\\f025\"; }\n\n.fa-volume-off:before {\n  content: \"\\f026\"; }\n\n.fa-volume-down:before {\n  content: \"\\f027\"; }\n\n.fa-volume-up:before {\n  content: \"\\f028\"; }\n\n.fa-qrcode:before {\n  content: \"\\f029\"; }\n\n.fa-barcode:before {\n  content: \"\\f02a\"; }\n\n.fa-tag:before {\n  content: \"\\f02b\"; }\n\n.fa-tags:before {\n  content: \"\\f02c\"; }\n\n.fa-book:before {\n  content: \"\\f02d\"; }\n\n.fa-bookmark:before {\n  content: \"\\f02e\"; }\n\n.fa-print:before {\n  content: \"\\f02f\"; }\n\n.fa-camera:before {\n  content: \"\\f030\"; }\n\n.fa-font:before {\n  content: \"\\f031\"; }\n\n.fa-bold:before {\n  content: \"\\f032\"; }\n\n.fa-italic:before {\n  content: \"\\f033\"; }\n\n.fa-text-height:before {\n  content: \"\\f034\"; }\n\n.fa-text-width:before {\n  content: \"\\f035\"; }\n\n.fa-align-left:before {\n  content: \"\\f036\"; }\n\n.fa-align-center:before {\n  content: \"\\f037\"; }\n\n.fa-align-right:before {\n  content: \"\\f038\"; }\n\n.fa-align-justify:before {\n  content: \"\\f039\"; }\n\n.fa-list:before {\n  content: \"\\f03a\"; }\n\n.fa-dedent:before,\n.fa-outdent:before {\n  content: \"\\f03b\"; }\n\n.fa-indent:before {\n  content: \"\\f03c\"; }\n\n.fa-video-camera:before {\n  content: \"\\f03d\"; }\n\n.fa-photo:before,\n.fa-image:before,\n.fa-picture-o:before {\n  content: \"\\f03e\"; }\n\n.fa-pencil:before {\n  content: \"\\f040\"; }\n\n.fa-map-marker:before {\n  content: \"\\f041\"; }\n\n.fa-adjust:before {\n  content: \"\\f042\"; }\n\n.fa-tint:before {\n  content: \"\\f043\"; }\n\n.fa-edit:before,\n.fa-pencil-square-o:before {\n  content: \"\\f044\"; }\n\n.fa-share-square-o:before {\n  content: \"\\f045\"; }\n\n.fa-check-square-o:before {\n  content: \"\\f046\"; }\n\n.fa-arrows:before {\n  content: \"\\f047\"; }\n\n.fa-step-backward:before {\n  content: \"\\f048\"; }\n\n.fa-fast-backward:before {\n  content: \"\\f049\"; }\n\n.fa-backward:before {\n  content: \"\\f04a\"; }\n\n.fa-play:before {\n  content: \"\\f04b\"; }\n\n.fa-pause:before {\n  content: \"\\f04c\"; }\n\n.fa-stop:before {\n  content: \"\\f04d\"; }\n\n.fa-forward:before {\n  content: \"\\f04e\"; }\n\n.fa-fast-forward:before {\n  content: \"\\f050\"; }\n\n.fa-step-forward:before {\n  content: \"\\f051\"; }\n\n.fa-eject:before {\n  content: \"\\f052\"; }\n\n.fa-chevron-left:before {\n  content: \"\\f053\"; }\n\n.fa-chevron-right:before {\n  content: \"\\f054\"; }\n\n.fa-plus-circle:before {\n  content: \"\\f055\"; }\n\n.fa-minus-circle:before {\n  content: \"\\f056\"; }\n\n.fa-times-circle:before {\n  content: \"\\f057\"; }\n\n.fa-check-circle:before {\n  content: \"\\f058\"; }\n\n.fa-question-circle:before {\n  content: \"\\f059\"; }\n\n.fa-info-circle:before {\n  content: \"\\f05a\"; }\n\n.fa-crosshairs:before {\n  content: \"\\f05b\"; }\n\n.fa-times-circle-o:before {\n  content: \"\\f05c\"; }\n\n.fa-check-circle-o:before {\n  content: \"\\f05d\"; }\n\n.fa-ban:before {\n  content: \"\\f05e\"; }\n\n.fa-arrow-left:before {\n  content: \"\\f060\"; }\n\n.fa-arrow-right:before {\n  content: \"\\f061\"; }\n\n.fa-arrow-up:before {\n  content: \"\\f062\"; }\n\n.fa-arrow-down:before {\n  content: \"\\f063\"; }\n\n.fa-mail-forward:before,\n.fa-share:before {\n  content: \"\\f064\"; }\n\n.fa-expand:before {\n  content: \"\\f065\"; }\n\n.fa-compress:before {\n  content: \"\\f066\"; }\n\n.fa-plus:before {\n  content: \"\\f067\"; }\n\n.fa-minus:before {\n  content: \"\\f068\"; }\n\n.fa-asterisk:before {\n  content: \"\\f069\"; }\n\n.fa-exclamation-circle:before {\n  content: \"\\f06a\"; }\n\n.fa-gift:before {\n  content: \"\\f06b\"; }\n\n.fa-leaf:before {\n  content: \"\\f06c\"; }\n\n.fa-fire:before {\n  content: \"\\f06d\"; }\n\n.fa-eye:before {\n  content: \"\\f06e\"; }\n\n.fa-eye-slash:before {\n  content: \"\\f070\"; }\n\n.fa-warning:before,\n.fa-exclamation-triangle:before {\n  content: \"\\f071\"; }\n\n.fa-plane:before {\n  content: \"\\f072\"; }\n\n.fa-calendar:before {\n  content: \"\\f073\"; }\n\n.fa-random:before {\n  content: \"\\f074\"; }\n\n.fa-comment:before {\n  content: \"\\f075\"; }\n\n.fa-magnet:before {\n  content: \"\\f076\"; }\n\n.fa-chevron-up:before {\n  content: \"\\f077\"; }\n\n.fa-chevron-down:before {\n  content: \"\\f078\"; }\n\n.fa-retweet:before {\n  content: \"\\f079\"; }\n\n.fa-shopping-cart:before {\n  content: \"\\f07a\"; }\n\n.fa-folder:before {\n  content: \"\\f07b\"; }\n\n.fa-folder-open:before {\n  content: \"\\f07c\"; }\n\n.fa-arrows-v:before {\n  content: \"\\f07d\"; }\n\n.fa-arrows-h:before {\n  content: \"\\f07e\"; }\n\n.fa-bar-chart-o:before,\n.fa-bar-chart:before {\n  content: \"\\f080\"; }\n\n.fa-twitter-square:before {\n  content: \"\\f081\"; }\n\n.fa-facebook-square:before {\n  content: \"\\f082\"; }\n\n.fa-camera-retro:before {\n  content: \"\\f083\"; }\n\n.fa-key:before {\n  content: \"\\f084\"; }\n\n.fa-gears:before,\n.fa-cogs:before {\n  content: \"\\f085\"; }\n\n.fa-comments:before {\n  content: \"\\f086\"; }\n\n.fa-thumbs-o-up:before {\n  content: \"\\f087\"; }\n\n.fa-thumbs-o-down:before {\n  content: \"\\f088\"; }\n\n.fa-star-half:before {\n  content: \"\\f089\"; }\n\n.fa-heart-o:before {\n  content: \"\\f08a\"; }\n\n.fa-sign-out:before {\n  content: \"\\f08b\"; }\n\n.fa-linkedin-square:before {\n  content: \"\\f08c\"; }\n\n.fa-thumb-tack:before {\n  content: \"\\f08d\"; }\n\n.fa-external-link:before {\n  content: \"\\f08e\"; }\n\n.fa-sign-in:before {\n  content: \"\\f090\"; }\n\n.fa-trophy:before {\n  content: \"\\f091\"; }\n\n.fa-github-square:before {\n  content: \"\\f092\"; }\n\n.fa-upload:before {\n  content: \"\\f093\"; }\n\n.fa-lemon-o:before {\n  content: \"\\f094\"; }\n\n.fa-phone:before {\n  content: \"\\f095\"; }\n\n.fa-square-o:before {\n  content: \"\\f096\"; }\n\n.fa-bookmark-o:before {\n  content: \"\\f097\"; }\n\n.fa-phone-square:before {\n  content: \"\\f098\"; }\n\n.fa-twitter:before {\n  content: \"\\f099\"; }\n\n.fa-facebook-f:before,\n.fa-facebook:before {\n  content: \"\\f09a\"; }\n\n.fa-github:before {\n  content: \"\\f09b\"; }\n\n.fa-unlock:before {\n  content: \"\\f09c\"; }\n\n.fa-credit-card:before {\n  content: \"\\f09d\"; }\n\n.fa-feed:before,\n.fa-rss:before {\n  content: \"\\f09e\"; }\n\n.fa-hdd-o:before {\n  content: \"\\f0a0\"; }\n\n.fa-bullhorn:before {\n  content: \"\\f0a1\"; }\n\n.fa-bell:before {\n  content: \"\\f0f3\"; }\n\n.fa-certificate:before {\n  content: \"\\f0a3\"; }\n\n.fa-hand-o-right:before {\n  content: \"\\f0a4\"; }\n\n.fa-hand-o-left:before {\n  content: \"\\f0a5\"; }\n\n.fa-hand-o-up:before {\n  content: \"\\f0a6\"; }\n\n.fa-hand-o-down:before {\n  content: \"\\f0a7\"; }\n\n.fa-arrow-circle-left:before {\n  content: \"\\f0a8\"; }\n\n.fa-arrow-circle-right:before {\n  content: \"\\f0a9\"; }\n\n.fa-arrow-circle-up:before {\n  content: \"\\f0aa\"; }\n\n.fa-arrow-circle-down:before {\n  content: \"\\f0ab\"; }\n\n.fa-globe:before {\n  content: \"\\f0ac\"; }\n\n.fa-wrench:before {\n  content: \"\\f0ad\"; }\n\n.fa-tasks:before {\n  content: \"\\f0ae\"; }\n\n.fa-filter:before {\n  content: \"\\f0b0\"; }\n\n.fa-briefcase:before {\n  content: \"\\f0b1\"; }\n\n.fa-arrows-alt:before {\n  content: \"\\f0b2\"; }\n\n.fa-group:before,\n.fa-users:before {\n  content: \"\\f0c0\"; }\n\n.fa-chain:before,\n.fa-link:before {\n  content: \"\\f0c1\"; }\n\n.fa-cloud:before {\n  content: \"\\f0c2\"; }\n\n.fa-flask:before {\n  content: \"\\f0c3\"; }\n\n.fa-cut:before,\n.fa-scissors:before {\n  content: \"\\f0c4\"; }\n\n.fa-copy:before,\n.fa-files-o:before {\n  content: \"\\f0c5\"; }\n\n.fa-paperclip:before {\n  content: \"\\f0c6\"; }\n\n.fa-save:before,\n.fa-floppy-o:before {\n  content: \"\\f0c7\"; }\n\n.fa-square:before {\n  content: \"\\f0c8\"; }\n\n.fa-navicon:before,\n.fa-reorder:before,\n.fa-bars:before {\n  content: \"\\f0c9\"; }\n\n.fa-list-ul:before {\n  content: \"\\f0ca\"; }\n\n.fa-list-ol:before {\n  content: \"\\f0cb\"; }\n\n.fa-strikethrough:before {\n  content: \"\\f0cc\"; }\n\n.fa-underline:before {\n  content: \"\\f0cd\"; }\n\n.fa-table:before {\n  content: \"\\f0ce\"; }\n\n.fa-magic:before {\n  content: \"\\f0d0\"; }\n\n.fa-truck:before {\n  content: \"\\f0d1\"; }\n\n.fa-pinterest:before {\n  content: \"\\f0d2\"; }\n\n.fa-pinterest-square:before {\n  content: \"\\f0d3\"; }\n\n.fa-google-plus-square:before {\n  content: \"\\f0d4\"; }\n\n.fa-google-plus:before {\n  content: \"\\f0d5\"; }\n\n.fa-money:before {\n  content: \"\\f0d6\"; }\n\n.fa-caret-down:before {\n  content: \"\\f0d7\"; }\n\n.fa-caret-up:before {\n  content: \"\\f0d8\"; }\n\n.fa-caret-left:before {\n  content: \"\\f0d9\"; }\n\n.fa-caret-right:before {\n  content: \"\\f0da\"; }\n\n.fa-columns:before {\n  content: \"\\f0db\"; }\n\n.fa-unsorted:before,\n.fa-sort:before {\n  content: \"\\f0dc\"; }\n\n.fa-sort-down:before,\n.fa-sort-desc:before {\n  content: \"\\f0dd\"; }\n\n.fa-sort-up:before,\n.fa-sort-asc:before {\n  content: \"\\f0de\"; }\n\n.fa-envelope:before {\n  content: \"\\f0e0\"; }\n\n.fa-linkedin:before {\n  content: \"\\f0e1\"; }\n\n.fa-rotate-left:before,\n.fa-undo:before {\n  content: \"\\f0e2\"; }\n\n.fa-legal:before,\n.fa-gavel:before {\n  content: \"\\f0e3\"; }\n\n.fa-dashboard:before,\n.fa-tachometer:before {\n  content: \"\\f0e4\"; }\n\n.fa-comment-o:before {\n  content: \"\\f0e5\"; }\n\n.fa-comments-o:before {\n  content: \"\\f0e6\"; }\n\n.fa-flash:before,\n.fa-bolt:before {\n  content: \"\\f0e7\"; }\n\n.fa-sitemap:before {\n  content: \"\\f0e8\"; }\n\n.fa-umbrella:before {\n  content: \"\\f0e9\"; }\n\n.fa-paste:before,\n.fa-clipboard:before {\n  content: \"\\f0ea\"; }\n\n.fa-lightbulb-o:before {\n  content: \"\\f0eb\"; }\n\n.fa-exchange:before {\n  content: \"\\f0ec\"; }\n\n.fa-cloud-download:before {\n  content: \"\\f0ed\"; }\n\n.fa-cloud-upload:before {\n  content: \"\\f0ee\"; }\n\n.fa-user-md:before {\n  content: \"\\f0f0\"; }\n\n.fa-stethoscope:before {\n  content: \"\\f0f1\"; }\n\n.fa-suitcase:before {\n  content: \"\\f0f2\"; }\n\n.fa-bell-o:before {\n  content: \"\\f0a2\"; }\n\n.fa-coffee:before {\n  content: \"\\f0f4\"; }\n\n.fa-cutlery:before {\n  content: \"\\f0f5\"; }\n\n.fa-file-text-o:before {\n  content: \"\\f0f6\"; }\n\n.fa-building-o:before {\n  content: \"\\f0f7\"; }\n\n.fa-hospital-o:before {\n  content: \"\\f0f8\"; }\n\n.fa-ambulance:before {\n  content: \"\\f0f9\"; }\n\n.fa-medkit:before {\n  content: \"\\f0fa\"; }\n\n.fa-fighter-jet:before {\n  content: \"\\f0fb\"; }\n\n.fa-beer:before {\n  content: \"\\f0fc\"; }\n\n.fa-h-square:before {\n  content: \"\\f0fd\"; }\n\n.fa-plus-square:before {\n  content: \"\\f0fe\"; }\n\n.fa-angle-double-left:before {\n  content: \"\\f100\"; }\n\n.fa-angle-double-right:before {\n  content: \"\\f101\"; }\n\n.fa-angle-double-up:before {\n  content: \"\\f102\"; }\n\n.fa-angle-double-down:before {\n  content: \"\\f103\"; }\n\n.fa-angle-left:before {\n  content: \"\\f104\"; }\n\n.fa-angle-right:before {\n  content: \"\\f105\"; }\n\n.fa-angle-up:before {\n  content: \"\\f106\"; }\n\n.fa-angle-down:before {\n  content: \"\\f107\"; }\n\n.fa-desktop:before {\n  content: \"\\f108\"; }\n\n.fa-laptop:before {\n  content: \"\\f109\"; }\n\n.fa-tablet:before {\n  content: \"\\f10a\"; }\n\n.fa-mobile-phone:before,\n.fa-mobile:before {\n  content: \"\\f10b\"; }\n\n.fa-circle-o:before {\n  content: \"\\f10c\"; }\n\n.fa-quote-left:before {\n  content: \"\\f10d\"; }\n\n.fa-quote-right:before {\n  content: \"\\f10e\"; }\n\n.fa-spinner:before {\n  content: \"\\f110\"; }\n\n.fa-circle:before {\n  content: \"\\f111\"; }\n\n.fa-mail-reply:before,\n.fa-reply:before {\n  content: \"\\f112\"; }\n\n.fa-github-alt:before {\n  content: \"\\f113\"; }\n\n.fa-folder-o:before {\n  content: \"\\f114\"; }\n\n.fa-folder-open-o:before {\n  content: \"\\f115\"; }\n\n.fa-smile-o:before {\n  content: \"\\f118\"; }\n\n.fa-frown-o:before {\n  content: \"\\f119\"; }\n\n.fa-meh-o:before {\n  content: \"\\f11a\"; }\n\n.fa-gamepad:before {\n  content: \"\\f11b\"; }\n\n.fa-keyboard-o:before {\n  content: \"\\f11c\"; }\n\n.fa-flag-o:before {\n  content: \"\\f11d\"; }\n\n.fa-flag-checkered:before {\n  content: \"\\f11e\"; }\n\n.fa-terminal:before {\n  content: \"\\f120\"; }\n\n.fa-code:before {\n  content: \"\\f121\"; }\n\n.fa-mail-reply-all:before,\n.fa-reply-all:before {\n  content: \"\\f122\"; }\n\n.fa-star-half-empty:before,\n.fa-star-half-full:before,\n.fa-star-half-o:before {\n  content: \"\\f123\"; }\n\n.fa-location-arrow:before {\n  content: \"\\f124\"; }\n\n.fa-crop:before {\n  content: \"\\f125\"; }\n\n.fa-code-fork:before {\n  content: \"\\f126\"; }\n\n.fa-unlink:before,\n.fa-chain-broken:before {\n  content: \"\\f127\"; }\n\n.fa-question:before {\n  content: \"\\f128\"; }\n\n.fa-info:before {\n  content: \"\\f129\"; }\n\n.fa-exclamation:before {\n  content: \"\\f12a\"; }\n\n.fa-superscript:before {\n  content: \"\\f12b\"; }\n\n.fa-subscript:before {\n  content: \"\\f12c\"; }\n\n.fa-eraser:before {\n  content: \"\\f12d\"; }\n\n.fa-puzzle-piece:before {\n  content: \"\\f12e\"; }\n\n.fa-microphone:before {\n  content: \"\\f130\"; }\n\n.fa-microphone-slash:before {\n  content: \"\\f131\"; }\n\n.fa-shield:before {\n  content: \"\\f132\"; }\n\n.fa-calendar-o:before {\n  content: \"\\f133\"; }\n\n.fa-fire-extinguisher:before {\n  content: \"\\f134\"; }\n\n.fa-rocket:before {\n  content: \"\\f135\"; }\n\n.fa-maxcdn:before {\n  content: \"\\f136\"; }\n\n.fa-chevron-circle-left:before {\n  content: \"\\f137\"; }\n\n.fa-chevron-circle-right:before {\n  content: \"\\f138\"; }\n\n.fa-chevron-circle-up:before {\n  content: \"\\f139\"; }\n\n.fa-chevron-circle-down:before {\n  content: \"\\f13a\"; }\n\n.fa-html5:before {\n  content: \"\\f13b\"; }\n\n.fa-css3:before {\n  content: \"\\f13c\"; }\n\n.fa-anchor:before {\n  content: \"\\f13d\"; }\n\n.fa-unlock-alt:before {\n  content: \"\\f13e\"; }\n\n.fa-bullseye:before {\n  content: \"\\f140\"; }\n\n.fa-ellipsis-h:before {\n  content: \"\\f141\"; }\n\n.fa-ellipsis-v:before {\n  content: \"\\f142\"; }\n\n.fa-rss-square:before {\n  content: \"\\f143\"; }\n\n.fa-play-circle:before {\n  content: \"\\f144\"; }\n\n.fa-ticket:before {\n  content: \"\\f145\"; }\n\n.fa-minus-square:before {\n  content: \"\\f146\"; }\n\n.fa-minus-square-o:before {\n  content: \"\\f147\"; }\n\n.fa-level-up:before {\n  content: \"\\f148\"; }\n\n.fa-level-down:before {\n  content: \"\\f149\"; }\n\n.fa-check-square:before {\n  content: \"\\f14a\"; }\n\n.fa-pencil-square:before {\n  content: \"\\f14b\"; }\n\n.fa-external-link-square:before {\n  content: \"\\f14c\"; }\n\n.fa-share-square:before {\n  content: \"\\f14d\"; }\n\n.fa-compass:before {\n  content: \"\\f14e\"; }\n\n.fa-toggle-down:before,\n.fa-caret-square-o-down:before {\n  content: \"\\f150\"; }\n\n.fa-toggle-up:before,\n.fa-caret-square-o-up:before {\n  content: \"\\f151\"; }\n\n.fa-toggle-right:before,\n.fa-caret-square-o-right:before {\n  content: \"\\f152\"; }\n\n.fa-euro:before,\n.fa-eur:before {\n  content: \"\\f153\"; }\n\n.fa-gbp:before {\n  content: \"\\f154\"; }\n\n.fa-dollar:before,\n.fa-usd:before {\n  content: \"\\f155\"; }\n\n.fa-rupee:before,\n.fa-inr:before {\n  content: \"\\f156\"; }\n\n.fa-cny:before,\n.fa-rmb:before,\n.fa-yen:before,\n.fa-jpy:before {\n  content: \"\\f157\"; }\n\n.fa-ruble:before,\n.fa-rouble:before,\n.fa-rub:before {\n  content: \"\\f158\"; }\n\n.fa-won:before,\n.fa-krw:before {\n  content: \"\\f159\"; }\n\n.fa-bitcoin:before,\n.fa-btc:before {\n  content: \"\\f15a\"; }\n\n.fa-file:before {\n  content: \"\\f15b\"; }\n\n.fa-file-text:before {\n  content: \"\\f15c\"; }\n\n.fa-sort-alpha-asc:before {\n  content: \"\\f15d\"; }\n\n.fa-sort-alpha-desc:before {\n  content: \"\\f15e\"; }\n\n.fa-sort-amount-asc:before {\n  content: \"\\f160\"; }\n\n.fa-sort-amount-desc:before {\n  content: \"\\f161\"; }\n\n.fa-sort-numeric-asc:before {\n  content: \"\\f162\"; }\n\n.fa-sort-numeric-desc:before {\n  content: \"\\f163\"; }\n\n.fa-thumbs-up:before {\n  content: \"\\f164\"; }\n\n.fa-thumbs-down:before {\n  content: \"\\f165\"; }\n\n.fa-youtube-square:before {\n  content: \"\\f166\"; }\n\n.fa-youtube:before {\n  content: \"\\f167\"; }\n\n.fa-xing:before {\n  content: \"\\f168\"; }\n\n.fa-xing-square:before {\n  content: \"\\f169\"; }\n\n.fa-youtube-play:before {\n  content: \"\\f16a\"; }\n\n.fa-dropbox:before {\n  content: \"\\f16b\"; }\n\n.fa-stack-overflow:before {\n  content: \"\\f16c\"; }\n\n.fa-instagram:before {\n  content: \"\\f16d\"; }\n\n.fa-flickr:before {\n  content: \"\\f16e\"; }\n\n.fa-adn:before {\n  content: \"\\f170\"; }\n\n.fa-bitbucket:before {\n  content: \"\\f171\"; }\n\n.fa-bitbucket-square:before {\n  content: \"\\f172\"; }\n\n.fa-tumblr:before {\n  content: \"\\f173\"; }\n\n.fa-tumblr-square:before {\n  content: \"\\f174\"; }\n\n.fa-long-arrow-down:before {\n  content: \"\\f175\"; }\n\n.fa-long-arrow-up:before {\n  content: \"\\f176\"; }\n\n.fa-long-arrow-left:before {\n  content: \"\\f177\"; }\n\n.fa-long-arrow-right:before {\n  content: \"\\f178\"; }\n\n.fa-apple:before {\n  content: \"\\f179\"; }\n\n.fa-windows:before {\n  content: \"\\f17a\"; }\n\n.fa-android:before {\n  content: \"\\f17b\"; }\n\n.fa-linux:before {\n  content: \"\\f17c\"; }\n\n.fa-dribbble:before {\n  content: \"\\f17d\"; }\n\n.fa-skype:before {\n  content: \"\\f17e\"; }\n\n.fa-foursquare:before {\n  content: \"\\f180\"; }\n\n.fa-trello:before {\n  content: \"\\f181\"; }\n\n.fa-female:before {\n  content: \"\\f182\"; }\n\n.fa-male:before {\n  content: \"\\f183\"; }\n\n.fa-gittip:before,\n.fa-gratipay:before {\n  content: \"\\f184\"; }\n\n.fa-sun-o:before {\n  content: \"\\f185\"; }\n\n.fa-moon-o:before {\n  content: \"\\f186\"; }\n\n.fa-archive:before {\n  content: \"\\f187\"; }\n\n.fa-bug:before {\n  content: \"\\f188\"; }\n\n.fa-vk:before {\n  content: \"\\f189\"; }\n\n.fa-weibo:before {\n  content: \"\\f18a\"; }\n\n.fa-renren:before {\n  content: \"\\f18b\"; }\n\n.fa-pagelines:before {\n  content: \"\\f18c\"; }\n\n.fa-stack-exchange:before {\n  content: \"\\f18d\"; }\n\n.fa-arrow-circle-o-right:before {\n  content: \"\\f18e\"; }\n\n.fa-arrow-circle-o-left:before {\n  content: \"\\f190\"; }\n\n.fa-toggle-left:before,\n.fa-caret-square-o-left:before {\n  content: \"\\f191\"; }\n\n.fa-dot-circle-o:before {\n  content: \"\\f192\"; }\n\n.fa-wheelchair:before {\n  content: \"\\f193\"; }\n\n.fa-vimeo-square:before {\n  content: \"\\f194\"; }\n\n.fa-turkish-lira:before,\n.fa-try:before {\n  content: \"\\f195\"; }\n\n.fa-plus-square-o:before {\n  content: \"\\f196\"; }\n\n.fa-space-shuttle:before {\n  content: \"\\f197\"; }\n\n.fa-slack:before {\n  content: \"\\f198\"; }\n\n.fa-envelope-square:before {\n  content: \"\\f199\"; }\n\n.fa-wordpress:before {\n  content: \"\\f19a\"; }\n\n.fa-openid:before {\n  content: \"\\f19b\"; }\n\n.fa-institution:before,\n.fa-bank:before,\n.fa-university:before {\n  content: \"\\f19c\"; }\n\n.fa-mortar-board:before,\n.fa-graduation-cap:before {\n  content: \"\\f19d\"; }\n\n.fa-yahoo:before {\n  content: \"\\f19e\"; }\n\n.fa-google:before {\n  content: \"\\f1a0\"; }\n\n.fa-reddit:before {\n  content: \"\\f1a1\"; }\n\n.fa-reddit-square:before {\n  content: \"\\f1a2\"; }\n\n.fa-stumbleupon-circle:before {\n  content: \"\\f1a3\"; }\n\n.fa-stumbleupon:before {\n  content: \"\\f1a4\"; }\n\n.fa-delicious:before {\n  content: \"\\f1a5\"; }\n\n.fa-digg:before {\n  content: \"\\f1a6\"; }\n\n.fa-pied-piper-pp:before {\n  content: \"\\f1a7\"; }\n\n.fa-pied-piper-alt:before {\n  content: \"\\f1a8\"; }\n\n.fa-drupal:before {\n  content: \"\\f1a9\"; }\n\n.fa-joomla:before {\n  content: \"\\f1aa\"; }\n\n.fa-language:before {\n  content: \"\\f1ab\"; }\n\n.fa-fax:before {\n  content: \"\\f1ac\"; }\n\n.fa-building:before {\n  content: \"\\f1ad\"; }\n\n.fa-child:before {\n  content: \"\\f1ae\"; }\n\n.fa-paw:before {\n  content: \"\\f1b0\"; }\n\n.fa-spoon:before {\n  content: \"\\f1b1\"; }\n\n.fa-cube:before {\n  content: \"\\f1b2\"; }\n\n.fa-cubes:before {\n  content: \"\\f1b3\"; }\n\n.fa-behance:before {\n  content: \"\\f1b4\"; }\n\n.fa-behance-square:before {\n  content: \"\\f1b5\"; }\n\n.fa-steam:before {\n  content: \"\\f1b6\"; }\n\n.fa-steam-square:before {\n  content: \"\\f1b7\"; }\n\n.fa-recycle:before {\n  content: \"\\f1b8\"; }\n\n.fa-automobile:before,\n.fa-car:before {\n  content: \"\\f1b9\"; }\n\n.fa-cab:before,\n.fa-taxi:before {\n  content: \"\\f1ba\"; }\n\n.fa-tree:before {\n  content: \"\\f1bb\"; }\n\n.fa-spotify:before {\n  content: \"\\f1bc\"; }\n\n.fa-deviantart:before {\n  content: \"\\f1bd\"; }\n\n.fa-soundcloud:before {\n  content: \"\\f1be\"; }\n\n.fa-database:before {\n  content: \"\\f1c0\"; }\n\n.fa-file-pdf-o:before {\n  content: \"\\f1c1\"; }\n\n.fa-file-word-o:before {\n  content: \"\\f1c2\"; }\n\n.fa-file-excel-o:before {\n  content: \"\\f1c3\"; }\n\n.fa-file-powerpoint-o:before {\n  content: \"\\f1c4\"; }\n\n.fa-file-photo-o:before,\n.fa-file-picture-o:before,\n.fa-file-image-o:before {\n  content: \"\\f1c5\"; }\n\n.fa-file-zip-o:before,\n.fa-file-archive-o:before {\n  content: \"\\f1c6\"; }\n\n.fa-file-sound-o:before,\n.fa-file-audio-o:before {\n  content: \"\\f1c7\"; }\n\n.fa-file-movie-o:before,\n.fa-file-video-o:before {\n  content: \"\\f1c8\"; }\n\n.fa-file-code-o:before {\n  content: \"\\f1c9\"; }\n\n.fa-vine:before {\n  content: \"\\f1ca\"; }\n\n.fa-codepen:before {\n  content: \"\\f1cb\"; }\n\n.fa-jsfiddle:before {\n  content: \"\\f1cc\"; }\n\n.fa-life-bouy:before,\n.fa-life-buoy:before,\n.fa-life-saver:before,\n.fa-support:before,\n.fa-life-ring:before {\n  content: \"\\f1cd\"; }\n\n.fa-circle-o-notch:before {\n  content: \"\\f1ce\"; }\n\n.fa-ra:before,\n.fa-resistance:before,\n.fa-rebel:before {\n  content: \"\\f1d0\"; }\n\n.fa-ge:before,\n.fa-empire:before {\n  content: \"\\f1d1\"; }\n\n.fa-git-square:before {\n  content: \"\\f1d2\"; }\n\n.fa-git:before {\n  content: \"\\f1d3\"; }\n\n.fa-y-combinator-square:before,\n.fa-yc-square:before,\n.fa-hacker-news:before {\n  content: \"\\f1d4\"; }\n\n.fa-tencent-weibo:before {\n  content: \"\\f1d5\"; }\n\n.fa-qq:before {\n  content: \"\\f1d6\"; }\n\n.fa-wechat:before,\n.fa-weixin:before {\n  content: \"\\f1d7\"; }\n\n.fa-send:before,\n.fa-paper-plane:before {\n  content: \"\\f1d8\"; }\n\n.fa-send-o:before,\n.fa-paper-plane-o:before {\n  content: \"\\f1d9\"; }\n\n.fa-history:before {\n  content: \"\\f1da\"; }\n\n.fa-circle-thin:before {\n  content: \"\\f1db\"; }\n\n.fa-header:before {\n  content: \"\\f1dc\"; }\n\n.fa-paragraph:before {\n  content: \"\\f1dd\"; }\n\n.fa-sliders:before {\n  content: \"\\f1de\"; }\n\n.fa-share-alt:before {\n  content: \"\\f1e0\"; }\n\n.fa-share-alt-square:before {\n  content: \"\\f1e1\"; }\n\n.fa-bomb:before {\n  content: \"\\f1e2\"; }\n\n.fa-soccer-ball-o:before,\n.fa-futbol-o:before {\n  content: \"\\f1e3\"; }\n\n.fa-tty:before {\n  content: \"\\f1e4\"; }\n\n.fa-binoculars:before {\n  content: \"\\f1e5\"; }\n\n.fa-plug:before {\n  content: \"\\f1e6\"; }\n\n.fa-slideshare:before {\n  content: \"\\f1e7\"; }\n\n.fa-twitch:before {\n  content: \"\\f1e8\"; }\n\n.fa-yelp:before {\n  content: \"\\f1e9\"; }\n\n.fa-newspaper-o:before {\n  content: \"\\f1ea\"; }\n\n.fa-wifi:before {\n  content: \"\\f1eb\"; }\n\n.fa-calculator:before {\n  content: \"\\f1ec\"; }\n\n.fa-paypal:before {\n  content: \"\\f1ed\"; }\n\n.fa-google-wallet:before {\n  content: \"\\f1ee\"; }\n\n.fa-cc-visa:before {\n  content: \"\\f1f0\"; }\n\n.fa-cc-mastercard:before {\n  content: \"\\f1f1\"; }\n\n.fa-cc-discover:before {\n  content: \"\\f1f2\"; }\n\n.fa-cc-amex:before {\n  content: \"\\f1f3\"; }\n\n.fa-cc-paypal:before {\n  content: \"\\f1f4\"; }\n\n.fa-cc-stripe:before {\n  content: \"\\f1f5\"; }\n\n.fa-bell-slash:before {\n  content: \"\\f1f6\"; }\n\n.fa-bell-slash-o:before {\n  content: \"\\f1f7\"; }\n\n.fa-trash:before {\n  content: \"\\f1f8\"; }\n\n.fa-copyright:before {\n  content: \"\\f1f9\"; }\n\n.fa-at:before {\n  content: \"\\f1fa\"; }\n\n.fa-eyedropper:before {\n  content: \"\\f1fb\"; }\n\n.fa-paint-brush:before {\n  content: \"\\f1fc\"; }\n\n.fa-birthday-cake:before {\n  content: \"\\f1fd\"; }\n\n.fa-area-chart:before {\n  content: \"\\f1fe\"; }\n\n.fa-pie-chart:before {\n  content: \"\\f200\"; }\n\n.fa-line-chart:before {\n  content: \"\\f201\"; }\n\n.fa-lastfm:before {\n  content: \"\\f202\"; }\n\n.fa-lastfm-square:before {\n  content: \"\\f203\"; }\n\n.fa-toggle-off:before {\n  content: \"\\f204\"; }\n\n.fa-toggle-on:before {\n  content: \"\\f205\"; }\n\n.fa-bicycle:before {\n  content: \"\\f206\"; }\n\n.fa-bus:before {\n  content: \"\\f207\"; }\n\n.fa-ioxhost:before {\n  content: \"\\f208\"; }\n\n.fa-angellist:before {\n  content: \"\\f209\"; }\n\n.fa-cc:before {\n  content: \"\\f20a\"; }\n\n.fa-shekel:before,\n.fa-sheqel:before,\n.fa-ils:before {\n  content: \"\\f20b\"; }\n\n.fa-meanpath:before {\n  content: \"\\f20c\"; }\n\n.fa-buysellads:before {\n  content: \"\\f20d\"; }\n\n.fa-connectdevelop:before {\n  content: \"\\f20e\"; }\n\n.fa-dashcube:before {\n  content: \"\\f210\"; }\n\n.fa-forumbee:before {\n  content: \"\\f211\"; }\n\n.fa-leanpub:before {\n  content: \"\\f212\"; }\n\n.fa-sellsy:before {\n  content: \"\\f213\"; }\n\n.fa-shirtsinbulk:before {\n  content: \"\\f214\"; }\n\n.fa-simplybuilt:before {\n  content: \"\\f215\"; }\n\n.fa-skyatlas:before {\n  content: \"\\f216\"; }\n\n.fa-cart-plus:before {\n  content: \"\\f217\"; }\n\n.fa-cart-arrow-down:before {\n  content: \"\\f218\"; }\n\n.fa-diamond:before {\n  content: \"\\f219\"; }\n\n.fa-ship:before {\n  content: \"\\f21a\"; }\n\n.fa-user-secret:before {\n  content: \"\\f21b\"; }\n\n.fa-motorcycle:before {\n  content: \"\\f21c\"; }\n\n.fa-street-view:before {\n  content: \"\\f21d\"; }\n\n.fa-heartbeat:before {\n  content: \"\\f21e\"; }\n\n.fa-venus:before {\n  content: \"\\f221\"; }\n\n.fa-mars:before {\n  content: \"\\f222\"; }\n\n.fa-mercury:before {\n  content: \"\\f223\"; }\n\n.fa-intersex:before,\n.fa-transgender:before {\n  content: \"\\f224\"; }\n\n.fa-transgender-alt:before {\n  content: \"\\f225\"; }\n\n.fa-venus-double:before {\n  content: \"\\f226\"; }\n\n.fa-mars-double:before {\n  content: \"\\f227\"; }\n\n.fa-venus-mars:before {\n  content: \"\\f228\"; }\n\n.fa-mars-stroke:before {\n  content: \"\\f229\"; }\n\n.fa-mars-stroke-v:before {\n  content: \"\\f22a\"; }\n\n.fa-mars-stroke-h:before {\n  content: \"\\f22b\"; }\n\n.fa-neuter:before {\n  content: \"\\f22c\"; }\n\n.fa-genderless:before {\n  content: \"\\f22d\"; }\n\n.fa-facebook-official:before {\n  content: \"\\f230\"; }\n\n.fa-pinterest-p:before {\n  content: \"\\f231\"; }\n\n.fa-whatsapp:before {\n  content: \"\\f232\"; }\n\n.fa-server:before {\n  content: \"\\f233\"; }\n\n.fa-user-plus:before {\n  content: \"\\f234\"; }\n\n.fa-user-times:before {\n  content: \"\\f235\"; }\n\n.fa-hotel:before,\n.fa-bed:before {\n  content: \"\\f236\"; }\n\n.fa-viacoin:before {\n  content: \"\\f237\"; }\n\n.fa-train:before {\n  content: \"\\f238\"; }\n\n.fa-subway:before {\n  content: \"\\f239\"; }\n\n.fa-medium:before {\n  content: \"\\f23a\"; }\n\n.fa-yc:before,\n.fa-y-combinator:before {\n  content: \"\\f23b\"; }\n\n.fa-optin-monster:before {\n  content: \"\\f23c\"; }\n\n.fa-opencart:before {\n  content: \"\\f23d\"; }\n\n.fa-expeditedssl:before {\n  content: \"\\f23e\"; }\n\n.fa-battery-4:before,\n.fa-battery:before,\n.fa-battery-full:before {\n  content: \"\\f240\"; }\n\n.fa-battery-3:before,\n.fa-battery-three-quarters:before {\n  content: \"\\f241\"; }\n\n.fa-battery-2:before,\n.fa-battery-half:before {\n  content: \"\\f242\"; }\n\n.fa-battery-1:before,\n.fa-battery-quarter:before {\n  content: \"\\f243\"; }\n\n.fa-battery-0:before,\n.fa-battery-empty:before {\n  content: \"\\f244\"; }\n\n.fa-mouse-pointer:before {\n  content: \"\\f245\"; }\n\n.fa-i-cursor:before {\n  content: \"\\f246\"; }\n\n.fa-object-group:before {\n  content: \"\\f247\"; }\n\n.fa-object-ungroup:before {\n  content: \"\\f248\"; }\n\n.fa-sticky-note:before {\n  content: \"\\f249\"; }\n\n.fa-sticky-note-o:before {\n  content: \"\\f24a\"; }\n\n.fa-cc-jcb:before {\n  content: \"\\f24b\"; }\n\n.fa-cc-diners-club:before {\n  content: \"\\f24c\"; }\n\n.fa-clone:before {\n  content: \"\\f24d\"; }\n\n.fa-balance-scale:before {\n  content: \"\\f24e\"; }\n\n.fa-hourglass-o:before {\n  content: \"\\f250\"; }\n\n.fa-hourglass-1:before,\n.fa-hourglass-start:before {\n  content: \"\\f251\"; }\n\n.fa-hourglass-2:before,\n.fa-hourglass-half:before {\n  content: \"\\f252\"; }\n\n.fa-hourglass-3:before,\n.fa-hourglass-end:before {\n  content: \"\\f253\"; }\n\n.fa-hourglass:before {\n  content: \"\\f254\"; }\n\n.fa-hand-grab-o:before,\n.fa-hand-rock-o:before {\n  content: \"\\f255\"; }\n\n.fa-hand-stop-o:before,\n.fa-hand-paper-o:before {\n  content: \"\\f256\"; }\n\n.fa-hand-scissors-o:before {\n  content: \"\\f257\"; }\n\n.fa-hand-lizard-o:before {\n  content: \"\\f258\"; }\n\n.fa-hand-spock-o:before {\n  content: \"\\f259\"; }\n\n.fa-hand-pointer-o:before {\n  content: \"\\f25a\"; }\n\n.fa-hand-peace-o:before {\n  content: \"\\f25b\"; }\n\n.fa-trademark:before {\n  content: \"\\f25c\"; }\n\n.fa-registered:before {\n  content: \"\\f25d\"; }\n\n.fa-creative-commons:before {\n  content: \"\\f25e\"; }\n\n.fa-gg:before {\n  content: \"\\f260\"; }\n\n.fa-gg-circle:before {\n  content: \"\\f261\"; }\n\n.fa-tripadvisor:before {\n  content: \"\\f262\"; }\n\n.fa-odnoklassniki:before {\n  content: \"\\f263\"; }\n\n.fa-odnoklassniki-square:before {\n  content: \"\\f264\"; }\n\n.fa-get-pocket:before {\n  content: \"\\f265\"; }\n\n.fa-wikipedia-w:before {\n  content: \"\\f266\"; }\n\n.fa-safari:before {\n  content: \"\\f267\"; }\n\n.fa-chrome:before {\n  content: \"\\f268\"; }\n\n.fa-firefox:before {\n  content: \"\\f269\"; }\n\n.fa-opera:before {\n  content: \"\\f26a\"; }\n\n.fa-internet-explorer:before {\n  content: \"\\f26b\"; }\n\n.fa-tv:before,\n.fa-television:before {\n  content: \"\\f26c\"; }\n\n.fa-contao:before {\n  content: \"\\f26d\"; }\n\n.fa-500px:before {\n  content: \"\\f26e\"; }\n\n.fa-amazon:before {\n  content: \"\\f270\"; }\n\n.fa-calendar-plus-o:before {\n  content: \"\\f271\"; }\n\n.fa-calendar-minus-o:before {\n  content: \"\\f272\"; }\n\n.fa-calendar-times-o:before {\n  content: \"\\f273\"; }\n\n.fa-calendar-check-o:before {\n  content: \"\\f274\"; }\n\n.fa-industry:before {\n  content: \"\\f275\"; }\n\n.fa-map-pin:before {\n  content: \"\\f276\"; }\n\n.fa-map-signs:before {\n  content: \"\\f277\"; }\n\n.fa-map-o:before {\n  content: \"\\f278\"; }\n\n.fa-map:before {\n  content: \"\\f279\"; }\n\n.fa-commenting:before {\n  content: \"\\f27a\"; }\n\n.fa-commenting-o:before {\n  content: \"\\f27b\"; }\n\n.fa-houzz:before {\n  content: \"\\f27c\"; }\n\n.fa-vimeo:before {\n  content: \"\\f27d\"; }\n\n.fa-black-tie:before {\n  content: \"\\f27e\"; }\n\n.fa-fonticons:before {\n  content: \"\\f280\"; }\n\n.fa-reddit-alien:before {\n  content: \"\\f281\"; }\n\n.fa-edge:before {\n  content: \"\\f282\"; }\n\n.fa-credit-card-alt:before {\n  content: \"\\f283\"; }\n\n.fa-codiepie:before {\n  content: \"\\f284\"; }\n\n.fa-modx:before {\n  content: \"\\f285\"; }\n\n.fa-fort-awesome:before {\n  content: \"\\f286\"; }\n\n.fa-usb:before {\n  content: \"\\f287\"; }\n\n.fa-product-hunt:before {\n  content: \"\\f288\"; }\n\n.fa-mixcloud:before {\n  content: \"\\f289\"; }\n\n.fa-scribd:before {\n  content: \"\\f28a\"; }\n\n.fa-pause-circle:before {\n  content: \"\\f28b\"; }\n\n.fa-pause-circle-o:before {\n  content: \"\\f28c\"; }\n\n.fa-stop-circle:before {\n  content: \"\\f28d\"; }\n\n.fa-stop-circle-o:before {\n  content: \"\\f28e\"; }\n\n.fa-shopping-bag:before {\n  content: \"\\f290\"; }\n\n.fa-shopping-basket:before {\n  content: \"\\f291\"; }\n\n.fa-hashtag:before {\n  content: \"\\f292\"; }\n\n.fa-bluetooth:before {\n  content: \"\\f293\"; }\n\n.fa-bluetooth-b:before {\n  content: \"\\f294\"; }\n\n.fa-percent:before {\n  content: \"\\f295\"; }\n\n.fa-gitlab:before {\n  content: \"\\f296\"; }\n\n.fa-wpbeginner:before {\n  content: \"\\f297\"; }\n\n.fa-wpforms:before {\n  content: \"\\f298\"; }\n\n.fa-envira:before {\n  content: \"\\f299\"; }\n\n.fa-universal-access:before {\n  content: \"\\f29a\"; }\n\n.fa-wheelchair-alt:before {\n  content: \"\\f29b\"; }\n\n.fa-question-circle-o:before {\n  content: \"\\f29c\"; }\n\n.fa-blind:before {\n  content: \"\\f29d\"; }\n\n.fa-audio-description:before {\n  content: \"\\f29e\"; }\n\n.fa-volume-control-phone:before {\n  content: \"\\f2a0\"; }\n\n.fa-braille:before {\n  content: \"\\f2a1\"; }\n\n.fa-assistive-listening-systems:before {\n  content: \"\\f2a2\"; }\n\n.fa-asl-interpreting:before,\n.fa-american-sign-language-interpreting:before {\n  content: \"\\f2a3\"; }\n\n.fa-deafness:before,\n.fa-hard-of-hearing:before,\n.fa-deaf:before {\n  content: \"\\f2a4\"; }\n\n.fa-glide:before {\n  content: \"\\f2a5\"; }\n\n.fa-glide-g:before {\n  content: \"\\f2a6\"; }\n\n.fa-signing:before,\n.fa-sign-language:before {\n  content: \"\\f2a7\"; }\n\n.fa-low-vision:before {\n  content: \"\\f2a8\"; }\n\n.fa-viadeo:before {\n  content: \"\\f2a9\"; }\n\n.fa-viadeo-square:before {\n  content: \"\\f2aa\"; }\n\n.fa-snapchat:before {\n  content: \"\\f2ab\"; }\n\n.fa-snapchat-ghost:before {\n  content: \"\\f2ac\"; }\n\n.fa-snapchat-square:before {\n  content: \"\\f2ad\"; }\n\n.fa-pied-piper:before {\n  content: \"\\f2ae\"; }\n\n.fa-first-order:before {\n  content: \"\\f2b0\"; }\n\n.fa-yoast:before {\n  content: \"\\f2b1\"; }\n\n.fa-themeisle:before {\n  content: \"\\f2b2\"; }\n\n.fa-google-plus-circle:before,\n.fa-google-plus-official:before {\n  content: \"\\f2b3\"; }\n\n.fa-fa:before,\n.fa-font-awesome:before {\n  content: \"\\f2b4\"; }\n\n.fa-handshake-o:before {\n  content: \"\\f2b5\"; }\n\n.fa-envelope-open:before {\n  content: \"\\f2b6\"; }\n\n.fa-envelope-open-o:before {\n  content: \"\\f2b7\"; }\n\n.fa-linode:before {\n  content: \"\\f2b8\"; }\n\n.fa-address-book:before {\n  content: \"\\f2b9\"; }\n\n.fa-address-book-o:before {\n  content: \"\\f2ba\"; }\n\n.fa-vcard:before,\n.fa-address-card:before {\n  content: \"\\f2bb\"; }\n\n.fa-vcard-o:before,\n.fa-address-card-o:before {\n  content: \"\\f2bc\"; }\n\n.fa-user-circle:before {\n  content: \"\\f2bd\"; }\n\n.fa-user-circle-o:before {\n  content: \"\\f2be\"; }\n\n.fa-user-o:before {\n  content: \"\\f2c0\"; }\n\n.fa-id-badge:before {\n  content: \"\\f2c1\"; }\n\n.fa-drivers-license:before,\n.fa-id-card:before {\n  content: \"\\f2c2\"; }\n\n.fa-drivers-license-o:before,\n.fa-id-card-o:before {\n  content: \"\\f2c3\"; }\n\n.fa-quora:before {\n  content: \"\\f2c4\"; }\n\n.fa-free-code-camp:before {\n  content: \"\\f2c5\"; }\n\n.fa-telegram:before {\n  content: \"\\f2c6\"; }\n\n.fa-thermometer-4:before,\n.fa-thermometer:before,\n.fa-thermometer-full:before {\n  content: \"\\f2c7\"; }\n\n.fa-thermometer-3:before,\n.fa-thermometer-three-quarters:before {\n  content: \"\\f2c8\"; }\n\n.fa-thermometer-2:before,\n.fa-thermometer-half:before {\n  content: \"\\f2c9\"; }\n\n.fa-thermometer-1:before,\n.fa-thermometer-quarter:before {\n  content: \"\\f2ca\"; }\n\n.fa-thermometer-0:before,\n.fa-thermometer-empty:before {\n  content: \"\\f2cb\"; }\n\n.fa-shower:before {\n  content: \"\\f2cc\"; }\n\n.fa-bathtub:before,\n.fa-s15:before,\n.fa-bath:before {\n  content: \"\\f2cd\"; }\n\n.fa-podcast:before {\n  content: \"\\f2ce\"; }\n\n.fa-window-maximize:before {\n  content: \"\\f2d0\"; }\n\n.fa-window-minimize:before {\n  content: \"\\f2d1\"; }\n\n.fa-window-restore:before {\n  content: \"\\f2d2\"; }\n\n.fa-times-rectangle:before,\n.fa-window-close:before {\n  content: \"\\f2d3\"; }\n\n.fa-times-rectangle-o:before,\n.fa-window-close-o:before {\n  content: \"\\f2d4\"; }\n\n.fa-bandcamp:before {\n  content: \"\\f2d5\"; }\n\n.fa-grav:before {\n  content: \"\\f2d6\"; }\n\n.fa-etsy:before {\n  content: \"\\f2d7\"; }\n\n.fa-imdb:before {\n  content: \"\\f2d8\"; }\n\n.fa-ravelry:before {\n  content: \"\\f2d9\"; }\n\n.fa-eercast:before {\n  content: \"\\f2da\"; }\n\n.fa-microchip:before {\n  content: \"\\f2db\"; }\n\n.fa-snowflake-o:before {\n  content: \"\\f2dc\"; }\n\n.fa-superpowers:before {\n  content: \"\\f2dd\"; }\n\n.fa-wpexplorer:before {\n  content: \"\\f2de\"; }\n\n.fa-meetup:before {\n  content: \"\\f2e0\"; }\n\n.sr-only {\n  position: absolute;\n  width: 1px;\n  height: 1px;\n  padding: 0;\n  margin: -1px;\n  overflow: hidden;\n  clip: rect(0, 0, 0, 0);\n  border: 0; }\n\n.sr-only-focusable:active,\n.sr-only-focusable:focus {\n  position: static;\n  width: auto;\n  height: auto;\n  margin: 0;\n  overflow: visible;\n  clip: auto; }\n\nhtml, body {\n  margin: 0px;\n  font-family: 'Roboto'; }\n\n.orchestrator {\n  max-width: 960px;\n  margin: 10px auto;\n  display: flex;\n  flex-direction: column;\n  align-items: stretch; }\n  .orchestrator table .center {\n    text-align: center; }\n  .orchestrator table .right {\n    text-align: right; }\n  .orchestrator table th.col-delay {\n    width: 100px; }\n  .orchestrator table th.col-fatal {\n    width: 100px; }\n  .orchestrator table th.col-revive {\n    width: 100px; }\n  .orchestrator table th.col-status {\n    width: 100px; }\n  .orchestrator table th.col-action {\n    width: 100px; }\n  .orchestrator table td.col-delay {\n    text-align: right; }\n  .orchestrator table td.col-fatal {\n    text-align: center; }\n  .orchestrator table td.col-revive {\n    text-align: center; }\n  .orchestrator table td.col-status {\n    text-align: center; }\n  .orchestrator table td.col-action {\n    text-align: center; }\n    .orchestrator table td.col-action button {\n      margin: 0px 2px; }\n", ""]);
// Exports
module.exports = exports;


/***/ }),
/* 31 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
// css base code, injected by the css-loader
// eslint-disable-next-line func-names
module.exports = function (useSourceMap) {
  var list = []; // return the list of modules as css string

  list.toString = function toString() {
    return this.map(function (item) {
      var content = cssWithMappingToString(item, useSourceMap);

      if (item[2]) {
        return "@media ".concat(item[2], " {").concat(content, "}");
      }

      return content;
    }).join('');
  }; // import a list of modules into the list
  // eslint-disable-next-line func-names


  list.i = function (modules, mediaQuery, dedupe) {
    if (typeof modules === 'string') {
      // eslint-disable-next-line no-param-reassign
      modules = [[null, modules, '']];
    }

    var alreadyImportedModules = {};

    if (dedupe) {
      for (var i = 0; i < this.length; i++) {
        // eslint-disable-next-line prefer-destructuring
        var id = this[i][0];

        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }

    for (var _i = 0; _i < modules.length; _i++) {
      var item = [].concat(modules[_i]);

      if (dedupe && alreadyImportedModules[item[0]]) {
        // eslint-disable-next-line no-continue
        continue;
      }

      if (mediaQuery) {
        if (!item[2]) {
          item[2] = mediaQuery;
        } else {
          item[2] = "".concat(mediaQuery, " and ").concat(item[2]);
        }
      }

      list.push(item);
    }
  };

  return list;
};

function cssWithMappingToString(item, useSourceMap) {
  var content = item[1] || ''; // eslint-disable-next-line prefer-destructuring

  var cssMapping = item[3];

  if (!cssMapping) {
    return content;
  }

  if (useSourceMap && typeof btoa === 'function') {
    var sourceMapping = toComment(cssMapping);
    var sourceURLs = cssMapping.sources.map(function (source) {
      return "/*# sourceURL=".concat(cssMapping.sourceRoot || '').concat(source, " */");
    });
    return [content].concat(sourceURLs).concat([sourceMapping]).join('\n');
  }

  return [content].join('\n');
} // Adapted from convert-source-map (MIT)


function toComment(sourceMap) {
  // eslint-disable-next-line no-undef
  var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap))));
  var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
  return "/*# ".concat(data, " */");
}

/***/ }),
/* 32 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


module.exports = function (url, options) {
  if (!options) {
    // eslint-disable-next-line no-param-reassign
    options = {};
  } // eslint-disable-next-line no-underscore-dangle, no-param-reassign


  url = url && url.__esModule ? url.default : url;

  if (typeof url !== 'string') {
    return url;
  } // If url is already wrapped in quotes, remove them


  if (/^['"].*['"]$/.test(url)) {
    // eslint-disable-next-line no-param-reassign
    url = url.slice(1, -1);
  }

  if (options.hash) {
    // eslint-disable-next-line no-param-reassign
    url += options.hash;
  } // Should url be wrapped?
  // See https://drafts.csswg.org/css-values-3/#urls


  if (/["'() \t\n]/.test(url) || options.needQuotes) {
    return "\"".concat(url.replace(/"/g, '\\"').replace(/\n/g, '\\n'), "\"");
  }

  return url;
};

/***/ }),
/* 33 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (__webpack_require__.p + "fonts/Roboto-Black.woff2");

/***/ }),
/* 34 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (__webpack_require__.p + "fonts/Roboto-BlackItalic.woff2");

/***/ }),
/* 35 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (__webpack_require__.p + "fonts/Roboto-Bold.woff2");

/***/ }),
/* 36 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (__webpack_require__.p + "fonts/Roboto-BoldItalic.woff2");

/***/ }),
/* 37 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (__webpack_require__.p + "fonts/Roboto-Medium.woff2");

/***/ }),
/* 38 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (__webpack_require__.p + "fonts/Roboto-MediumItalic.woff2");

/***/ }),
/* 39 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (__webpack_require__.p + "fonts/Roboto-Regular.woff2");

/***/ }),
/* 40 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (__webpack_require__.p + "fonts/Roboto-RegularItalic.woff2");

/***/ }),
/* 41 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (__webpack_require__.p + "fonts/Roboto-Light.woff2");

/***/ }),
/* 42 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (__webpack_require__.p + "fonts/Roboto-LightItalic.woff2");

/***/ }),
/* 43 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (__webpack_require__.p + "fonts/Roboto-Thin.woff2");

/***/ }),
/* 44 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (__webpack_require__.p + "fonts/Roboto-ThinItalic.woff2");

/***/ }),
/* 45 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (__webpack_require__.p + "fonts/FontAwesome-webfont.woff2");

/***/ })
/******/ ]);
//# sourceMappingURL=orchestrator.js.map