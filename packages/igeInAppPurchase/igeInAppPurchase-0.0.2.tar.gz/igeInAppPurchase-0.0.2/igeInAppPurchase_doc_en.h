PyDoc_STRVAR(getProductsList_doc,
             "Query all the IAP products available on the store.\n"
             "\n"
             "\n"
             "getProductsList(callback);\n"
             "\n"
             "Parameters\n"
             "----------\n"
             "    callback(status, products) : func\n"
             "        Callback function, to retrieve the data from store.\n"
             "        Parameters\n"
             "        ----------\n"
             "            status: int\n"
             "                Querying status.\n"
             "            products: list<Product>\n"
             "                List of available products or empty list.\n");

PyDoc_STRVAR(getPurchasedProducts_doc,
             "Query all the products that were purchased.\n"
             "\n"
             "\n"
             "getPurchasedProducts(callback);\n"
             "\n"
             "Notice\n"
             "----------\n"
             "    Apple App Store : only return non-consumable or auto renewed supscription\n"
             "    Google Play Store : TBD\n"
             "\n"
             "Parameters\n"
             "----------\n"
             "    callback : func\n"
             "        Callback function, to retrieve the data from store.\n");

PyDoc_STRVAR(purchaseProduct_doc,
             "Send purchasing request to store.\n"
             "\n"
             "\n"
             "purchaseProduct(productId, callback);\n"
             "\n"
             "Notice\n"
             "----------\n"
             "    Apple App Store : only return non-consumable or auto renewed supscription\n"
             "    Google Play Store : TBD\n"
             "\n"
             "Parameters\n"
             "----------\n"
             "    callback(status, products) : func\n"
             "        Callback function, to retrieve the data from store.\n"
             "        Parameters\n"
             "        ----------\n"
             "            status: int\n"
             "                Purchasing status.\n"
             "            products: list<Product>\n"
             "                List of purchasing products or empty list.\n");

PyDoc_STRVAR(restorePurchases_doc,
             "Restore the previous purchase.\n"
             "\n"
             "\n"
             "restorePurchases(callback);\n"
             "\n"
             "Notice\n"
             "----------\n"
             "    Apple App Store : only for non-consumable or auto renewed supscription\n"
             "    Google Play Store : TBD\n"
             "\n"
             "Parameters\n"
             "----------\n"
             "    callback(status, products) : func\n"
             "        Callback function, to retrieve the data from store.\n"
             "        Parameters\n"
             "        ----------\n"
             "            status: int\n"
             "                Restoring status.\n"
             "            products: list<Product>\n"
             "                List of purchasing products or empty list.\n");

PyDoc_STRVAR(init_doc,
             "Initialize IAP module.\n"
             "\n"
             "\n"
             "init('sandbox');\n"
             "\n"
             "Parameters\n"
             "----------\n"
             "    environment : string\n"
             "        InAppPurchase environment: default 'production', set to 'sandbox' for validating with testing accounts.\n");

PyDoc_STRVAR(update_doc,
             "Update IAP processes.\n"
             "\n"
             "\n"
             "update();\n");

PyDoc_STRVAR(destroy_doc,
             "Destroy IAP module.\n"
             "\n"
             "\n"
             "destroy();\n");
