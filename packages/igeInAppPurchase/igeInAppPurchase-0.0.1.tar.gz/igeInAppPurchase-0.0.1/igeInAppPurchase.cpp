#include <memory>
#include <mutex>

#include <Python.h>

#include "InAppPurchase.h"
#include "igeInAppPurchase_doc_en.h"

enum class IAPFuncType
{
    GetProductsList = 0,
    PurchaseProduct,
    RestorePurchases,
    GetPurchasedProducts,
};

struct IAPCallbackParams
{
    IAPFuncType funcType;
    int status;
    std::vector<IAPProduct *> products;

    IAPCallbackParams(IAPFuncType funcType, int status, const std::vector<IAPProduct *> &products)
    {
        this->funcType = funcType;
        this->status = status;
        for (int i = 0; i < products.size(); ++i)
        {
            this->products.push_back(products[i]);
        }
    }
};

typedef struct
{
    PyObject_HEAD
        IAPProduct *product;
} product_obj;

extern PyTypeObject ProductType;

static std::shared_ptr<InAppPurchase> gIAP = nullptr;
static PyObject *py_getProductsListCB = nullptr;
static PyObject *py_purchaseProductCB = nullptr;
static PyObject *py_restorePurchasesCB = nullptr;
static PyObject *py_getPurchasedProductsCB = nullptr;

static std::mutex callbackParams_mtx;
static std::vector<IAPCallbackParams> callbackParams;

static void getProductsListCB(int status, const std::vector<IAPProduct *> &products)
{
    std::lock_guard<std::mutex> uniq_lk(callbackParams_mtx);
    callbackParams.push_back({IAPFuncType::GetProductsList, status, products});
}

static void purchaseProductCB(int status, const std::vector<IAPProduct *> &products)
{
    std::lock_guard<std::mutex> uniq_lk(callbackParams_mtx);
    callbackParams.push_back({IAPFuncType::PurchaseProduct, status, products});
}

static void restorePurchasesCB(int status, const std::vector<IAPProduct *> &products)
{
    std::lock_guard<std::mutex> uniq_lk(callbackParams_mtx);
    callbackParams.push_back({IAPFuncType::RestorePurchases, status, products});
}

static void getPurchasedProductsCB(int status, const std::vector<IAPProduct *> &products)
{
    std::lock_guard<std::mutex> uniq_lk(callbackParams_mtx);
    callbackParams.push_back({IAPFuncType::GetPurchasedProducts, status, products});
}

static PyObject *iap_init(PyObject *self, PyObject *args)
{
    char *env = (char *)"production";
    if (!PyArg_ParseTuple(args, "|s", &env))
    {
        PyErr_SetString(PyExc_TypeError, "Parameters are not corrects");
        return NULL;
    }
    gIAP->init(std::string(env));
    Py_RETURN_NONE;
}

static PyObject *iap_update(PyObject *self)
{
    std::lock_guard<std::mutex> uniq_lk(callbackParams_mtx);
    for (auto it = callbackParams.begin(); it != callbackParams.end(); it++)
    {
        PyObject *list = PyList_New(0);
        for (int i = 0; i < it->products.size(); ++i)
        {
            product_obj *obj = PyObject_New(product_obj, &ProductType);
            obj->product = new IAPProduct(it->products[i]->id,
                                          it->products[i]->title,
                                          it->products[i]->description,
                                          it->products[i]->locale,
                                          it->products[i]->price,
                                          it->products[i]->discount);
            PyList_Append(list, (PyObject *)obj);
            Py_DECREF(obj);
            delete it->products[i];
        }

        PyObject *arglist = Py_BuildValue("(iO)", it->status, list);
        PyObject *result = nullptr;
        if (it->funcType == IAPFuncType::GetProductsList)
        {
            result = PyEval_CallObject(py_getProductsListCB, arglist);
        }
        else if (it->funcType == IAPFuncType::PurchaseProduct)
        {
            result = PyEval_CallObject(py_purchaseProductCB, arglist);
        }
        else if (it->funcType == IAPFuncType::RestorePurchases)
        {
            result = PyEval_CallObject(py_restorePurchasesCB, arglist);
        }
        else if (it->funcType == IAPFuncType::GetPurchasedProducts)
        {
            result = PyEval_CallObject(py_getPurchasedProductsCB, arglist);
        }
        Py_DECREF(arglist);
        Py_XDECREF(result);
    }
    callbackParams.clear();
    Py_RETURN_NONE;
}

static PyObject *iap_destroy(PyObject *self)
{
    gIAP->destroy();
    gIAP = nullptr;
    Py_RETURN_NONE;
}

static PyObject *iap_getProductsList(PyObject *self, PyObject *args)
{
    PyObject *py_cb;

    if (!PyArg_ParseTuple(args, "O", &py_cb))
    {
        PyErr_SetString(PyExc_TypeError, "Callback function was not set!");
        return NULL;
    }

    if (!PyCallable_Check(py_cb))
    {
        PyErr_SetString(PyExc_TypeError, "Callback function must be a callable object!");
        return NULL;
    }
    Py_XINCREF(py_cb);
    py_getProductsListCB = py_cb;

    gIAP->getProductsList(getProductsListCB);
    Py_RETURN_NONE;
}

static PyObject *iap_getPurchasedProducts(PyObject *self, PyObject *args)
{
    PyObject *py_cb;

    if (!PyArg_ParseTuple(args, "O", &py_cb))
    {
        PyErr_SetString(PyExc_TypeError, "Callback function was not set!");
        return NULL;
    }

    if (!PyCallable_Check(py_cb))
    {
        PyErr_SetString(PyExc_TypeError, "Callback function must be a callable object!");
        return NULL;
    }
    Py_XINCREF(py_cb);
    py_getPurchasedProductsCB = py_cb;

    gIAP->getPurchasedProducts(getPurchasedProductsCB);
    Py_RETURN_NONE;
}

static PyObject *iap_purchaseProduct(PyObject *self, PyObject *args)
{
    char *productId;
    PyObject *py_cb;

    if (!PyArg_ParseTuple(args, "sO", &productId, &py_cb))
    {
        PyErr_SetString(PyExc_TypeError, "Parameters are not corrects: sO");
        return NULL;
    }

    if (!PyCallable_Check(py_cb))
    {
        PyErr_SetString(PyExc_TypeError, "Callback function must be a callable object!");
        return NULL;
    }
    Py_XINCREF(py_cb);
    py_purchaseProductCB = py_cb;

    gIAP->purchaseProduct(std::string(productId), purchaseProductCB);
    Py_RETURN_NONE;
}

static PyObject *iap_restorePurchases(PyObject *self, PyObject *args)
{
    PyObject *py_cb;

    if (!PyArg_ParseTuple(args, "O", &py_cb))
    {
        PyErr_SetString(PyExc_TypeError, "Callback function was not set!");
        return NULL;
    }

    if (!PyCallable_Check(py_cb))
    {
        PyErr_SetString(PyExc_TypeError, "Callback function must be a callable object!");
        return NULL;
    }
    Py_XINCREF(py_cb);
    py_restorePurchasesCB = py_cb;

    gIAP->restorePurchases(restorePurchasesCB);
    Py_RETURN_NONE;
}

static PyMethodDef iap_methods[] = {
    {"getProductsList", (PyCFunction)iap_getProductsList, METH_VARARGS, getProductsList_doc},
    {"getPurchasedProducts", (PyCFunction)iap_getPurchasedProducts, METH_VARARGS, getPurchasedProducts_doc},
    {"purchaseProduct", (PyCFunction)iap_purchaseProduct, METH_VARARGS, purchaseProduct_doc},
    {"restorePurchases", (PyCFunction)iap_restorePurchases, METH_VARARGS, restorePurchases_doc},
    {"init", (PyCFunction)iap_init, METH_VARARGS, init_doc},
    {"update", (PyCFunction)iap_update, METH_NOARGS, update_doc},
    {"destroy", (PyCFunction)iap_destroy, METH_NOARGS, destroy_doc},
    {nullptr, nullptr, 0, nullptr}};

static PyModuleDef iap_module = {
    PyModuleDef_HEAD_INIT,
    "igeInAppPurchase",
    "InAppPurchase module",
    0,
    iap_methods};

PyMODINIT_FUNC PyInit_igeInAppPurchase()
{
    gIAP = std::make_shared<InAppPurchase>();
    PyObject *module = PyModule_Create(&iap_module);

    if (PyType_Ready(&ProductType) < 0)
        return NULL;
    Py_INCREF(&ProductType);
    PyModule_AddObject(module, "Product", (PyObject *)&ProductType);

    return module;
}

PyObject *product_new(PyTypeObject *type, PyObject *args, PyObject *kw)
{
    product_obj *self = (product_obj *)type->tp_alloc(type, 0);
    self->product = nullptr;
    return (PyObject *)self;
}

void product_dealloc(product_obj *self)
{
    Py_TYPE(self)->tp_free(self);
}

PyObject *product_str(product_obj *self)
{
    return PyUnicode_FromString("Product Object");
}

PyObject *product_getId(product_obj *self)
{
    return PyUnicode_FromString(self->product->id.c_str());
}

int product_setId(product_obj *self, PyObject *value)
{
    self->product->id = std::string(PyUnicode_AsUTF8(value));
    return 0;
}

PyObject *product_getTitle(product_obj *self)
{
    return PyUnicode_FromString(self->product->title.c_str());
}

int product_setTitle(product_obj *self, PyObject *value)
{
    self->product->title = std::string(PyUnicode_AsUTF8(value));
    return 0;
}

PyObject *product_getDescription(product_obj *self)
{
    return PyUnicode_FromString(self->product->description.c_str());
}

int product_setDescription(product_obj *self, PyObject *value)
{
    self->product->description = std::string(PyUnicode_AsUTF8(value));
    return 0;
}

PyObject *product_getLocale(product_obj *self)
{
    return PyUnicode_FromString(self->product->locale.c_str());
}

int product_setLocale(product_obj *self, PyObject *value)
{
    self->product->locale = std::string(PyUnicode_AsUTF8(value));
    return 0;
}

PyObject *product_getPrice(product_obj *self)
{
    return PyFloat_FromDouble(self->product->price);
}

int product_setPrice(product_obj *self, PyObject *value)
{
    self->product->price = PyFloat_AsDouble(value);
    return 0;
}

PyObject *product_getDiscount(product_obj *self)
{
    return PyFloat_FromDouble(self->product->discount);
}

int product_setDiscount(product_obj *self, PyObject *value)
{
    self->product->discount = PyFloat_AsDouble(value);
    return 0;
}

PyMethodDef product_methods[] = {
    {NULL, NULL}};

PyGetSetDef product_getsets[] = {
    {const_cast<char *>("id"), (getter)product_getId, (setter)product_setId, "Product's ID", NULL},
    {const_cast<char *>("title"), (getter)product_getTitle, (setter)product_setTitle, "Product's Title", NULL},
    {const_cast<char *>("description"), (getter)product_getDescription, (setter)product_setDescription, "Product's Description", NULL},
    {const_cast<char *>("locale"), (getter)product_getLocale, (setter)product_setLocale, "Product's Locale", NULL},
    {const_cast<char *>("price"), (getter)product_getPrice, (setter)product_setPrice, "Product's Price", NULL},
    {const_cast<char *>("discount"), (getter)product_getDiscount, (setter)product_setDiscount, "Product's Discount", NULL},
    {NULL, NULL}};

PyTypeObject ProductType = {
    PyVarObject_HEAD_INIT(NULL, 0) "igeInAppPurchase.Product", /* tp_name */
    sizeof(product_obj),                                       /* tp_basicsize */
    0,                                                         /* tp_itemsize */
    (destructor)product_dealloc,                               /* tp_dealloc */
    0,                                                         /* tp_print */
    0,                                                         /* tp_getattr */
    0,                                                         /* tp_setattr */
    0,                                                         /* tp_reserved */
    0,                                                         /* tp_repr */
    0,                                                         /* tp_as_number */
    0,                                                         /* tp_as_sequence */
    0,                                                         /* tp_as_mapping */
    0,                                                         /* tp_hash */
    0,                                                         /* tp_call */
    (reprfunc)product_str,                                     /* tp_str */
    0,                                                         /* tp_getattro */
    0,                                                         /* tp_setattro */
    0,                                                         /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                                        /* tp_flags */
    0,                                                         /* tp_doc */
    0,                                                         /* tp_traverse */
    0,                                                         /* tp_clear */
    0,                                                         /* tp_richcompare */
    0,                                                         /* tp_weaklistoffset */
    0,                                                         /* tp_iter */
    0,                                                         /* tp_iternext */
    product_methods,                                           /* tp_methods */
    0,                                                         /* tp_members */
    product_getsets,                                           /* tp_getset */
    0,                                                         /* tp_base */
    0,                                                         /* tp_dict */
    0,                                                         /* tp_descr_get */
    0,                                                         /* tp_descr_set */
    0,                                                         /* tp_dictoffset */
    0,                                                         /* tp_init */
    0,                                                         /* tp_alloc */
    product_new,                                               /* tp_new */
    0,                                                         /* tp_free */
};
