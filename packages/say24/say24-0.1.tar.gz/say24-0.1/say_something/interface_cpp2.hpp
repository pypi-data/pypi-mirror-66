#pragma once
#include "libset_core.h"

#ifdef __cplusplus
extern "C" {
#endif

    /*
	For Both Investor and MarketRep
	*/
	CreateContext_return iCreateContext(
        char* appID, 
        char* appSecret, 
        char* brokerID
        );
	/*
	For Investor Derivatives
	*/
	GetInvestorDerivativesPortfolios_return iGetInvestorDerivativesPortfolios(
        Context* c, 
        char* accountNO
        );

	GetInvestorDerivativesAccountInfo_return iGetInvestorDerivativesAccountInfo(
        Context* c, 
        char* accountNO
        );

	GetInvestorDerivativesOrders_return iGetInvestorDerivativesOrders(
        Context* c, 
        char* accountNO
        );

	GetInvestorDerivativesOrder_return iGetInvestorDerivativesOrder(
        Context* c, 
        char* accountNO, 
        int orderNO
        );

	GetInvestorDerivativesTrades_return iGetInvestorDerivativesTrades(
        Context* c, 
        char* accountNO
        );

    PlaceInvestorDerivativesOrder_return iPlaceInvestorDerivativesOrder(
        Context* c, 
        char* accountNO,
        RequestPlaceOrder* placeOrder
        );

    Error iCancelInvestorDerivativesOrder(
        Context* c,
        char* accountNO,
        int orderNO,
        RequestCancelOrder* cancelOrder
        );

    Error iCancelInvestorDerivativesOrders(
        Context* c,
        char* accountNO,
        int* ordersNO,
        int sizeOrdersNo,
        char* pin
        );

    Error iChangeInvestorDerivativesOrder(
        Context* c, 
        char* accountNO, 
        int orderNO, 
        RequestChangeOrder* changeOrder
        );
	/*
	End Investor Derivatives
	*/

    /*
    For MarketRep Derivatives
    */
    GetMarketRepDerivativesOrders_return iGetMarketRepDerivativesOrders(
        Context* c, 
        char* accountNO
        );

    GetMarketRepDerivativesOrder_return iGetMarketRepDerivativesOrder(
        Context* c, 
        int orderNO
        );

    GetMarketRepDerivativesPortfolios_return iGetMarketRepDerivativesPortfolios(
        Context* c, 
        char* accountNO
        );

    GetMarketRepDerivativesTrades_return iGetMarketRepDerivativesTrades(
        Context* c, 
        char* accountNO
        );

    PlaceMarketRepDerivativesOrder_return iPlaceMarketRepDerivativesOrder(
        Context* c, 
        char* accountNO,
        RequestPlaceMarketRepOrder* placeOrder
        );

    Error iCancelMarketRepDerivativesOrder(
        Context* c,
        char* accountNO,
        int orderNO
        );

    Error iCancelMarketRepDerivativesOrders(
        Context* c,
        char* accountNO,
        int* ordersNO,
        int sizeOrdersNo
        );

    Error iChangeMarketRepDerivativesOrder(
        Context* c, 
        char* accountNO, 
        int orderNO, 
        RequestChangeMarketRepOrder* changeOrder
        );
        
    Error iPlaceMarketRepDerivativesTradeReport(
        Context* c, 
        RequestPlaceTradeReport* tradeReport
        );
    /*
	End MarketRep Derivatives
	*/

#ifdef __cplusplus
}
#endif