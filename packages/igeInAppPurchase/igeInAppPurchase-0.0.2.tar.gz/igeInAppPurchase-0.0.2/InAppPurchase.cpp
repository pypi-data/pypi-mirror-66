#include "InAppPurchase.h"

InAppPurchase::InAppPurchase()
{
    mImpl = std::make_shared<InAppPurchaseImpl>();
}

InAppPurchase::~InAppPurchase()
{
    mImpl = nullptr;
}

void InAppPurchase::getProductsList(GetProductsListCB cb)
{
    mImpl->getProductsList(cb);
}

void InAppPurchase::getPurchasedProducts(GetPurchasedProductsCB cb)
{
    mImpl->getPurchasedProducts(cb);
}

void InAppPurchase::purchaseProduct(std::string productId, PurchaseProductCB cb)
{
    mImpl->purchaseProduct(productId, cb);
}

void InAppPurchase::restorePurchases(RestorePurchasesCB cb)
{
    mImpl->restorePurchases(cb);
}

void InAppPurchase::init(std::string env)
{
    mImpl->init(env);
}

void InAppPurchase::destroy()
{
    mImpl->destroy();
}