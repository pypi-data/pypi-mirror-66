#ifndef C_MODELS
#define C_MODELS
#include <stdbool.h>

typedef struct defaultResponse {
	bool success;
	int status_code;
	char* message;
} DefaultResponse;

typedef struct error {
	char* message;
} Error;

typedef struct context {
	char* app_id;
	char* app_secret;
	char* broker_id;
	char* access_token;
	char* refresh_token;
} Context;

typedef struct contextResponse {
	bool success;
	int status_code;
	Context data;
	char* message;
} ContextResponse;

/*
	Account Structs
*/
typedef struct accountInfo {
	double credit_line;
	double excess_equity;
	double cash_balance;
	double equity;
	double total_mr;
	double total_mm;
	char* call_force_flag;
	double call_force_margin;
} AccountInfo;

typedef struct getAccountInfoResponse {
	bool success;
	int status_code;
	AccountInfo data;
	char* message;
} GetAccountInfoResponse;
/*
	End of Account Structs
*/

/*
	Portfolio Structs
*/
typedef struct portfolio {
	char* account_no; 
	long actual_long_position;    
	long actual_short_position;    
	char* as_of_date_xrt; 
	long available_long_position;    
	long available_short_position;    
	double avg_xrt_long;
	double avg_xrt_long_cost;
	double avg_xrt_short;
	double avg_xrt_short_cost;
	char* broker_id; 
	long close_long_position;    
	long close_short_position;    
	char* currency; 
	double current_xrt;
	bool has_long_position;   
	bool has_short_position;   
	char* last_trading_date; 
	double long_avg_cost;
	double long_avg_price;
	double market_price;
	double multiplier;
	long open_long_position;    
	long open_short_position;    
	double realized_pl;
	double realized_pl_by_cost;
	double realized_pl_by_cost_currency;
	double realized_pl_currency;
	char* security_type; 
	double short_avg_cost;
	double short_avg_price;
	double start_long_cost;
	long start_long_position;    
	double start_long_price;
	double start_short_cost;
	long start_short_position;    
	double start_short_price;
	double start_xrt_long;
	double start_xrt_long_cost;
	double start_xrt_short;
	double start_xrt_short_cost;
	char* symbol; 
	char* underlying; 
} Portfolio;
/*
	End of Portfolio Structs
*/

/*
	Trade Structs
*/
typedef struct trade {
	char* account_no;
	char* broker_id;
	char* currency;
	char* deal_no;
	char* entry_id;
	char* ledger_date;
	long ledger_seq;
	char* ledger_time;
	double multiplier;
	char* open_close;
	long order_no;
	double px;
	long qty;
	long rectified_qty;
	char* ref_ledger_date;
	long ref_ledger_seq;
	char* reject_code;
	char* reject_reason;
	char* side;
	char* status;
	char* symbol;
	char* trade_date;
	char* trade_no;
	char* trade_time;
	char* trade_type;
} Trade;
/*
	End of Trade Structs
*/

/*
	Order Structs
*/
typedef struct order {
	char* account_no;
	int balance_qty;
	int cancel_qty;
	char* entry_date;
	char* entry_id;
	char* entry_time;
	char* is_stop_order_not_activate;
	int match_qty;
	int order_no;
	char* position;
	double price;
	char* price_type;
	int qty;
	int reject_code;
	char* reject_reason;
	char* show_status;
	char* side;
	char* status;
	char* status_meaning;
	char* symbol;
	char* tfx_order_no;
	char* trigger_condition;
	double trigger_price;
	char* trigger_symbol;
	char* validity;
	int version;
} Order;

typedef struct requestPlaceOrder {
	bool bypass_warning;
	char* pin;
	char *position;
	double price;
	char* price_type;
	char* side;
	char* stop_condition;
	double stop_price;
	char *stop_symbol;
	char* symbol;
	char *validity_type;
	int volume;
} RequestPlaceOrder;

typedef struct responsePlaceOrder {
	int order_no;
} ResponsePlaceOrder;

typedef struct requestCancelOrder {
	char* pin;
} RequestCancelOrder;

// typedef struct requestCancelOrders {
// 	int orders[];
// 	char* pin;
// } RequestCancelOrders;

typedef struct requestChangeOrder {
	char* new_position;
	char* new_price_type;
	double new_price;
	int new_volume;
	char* pin;
} RequestChangeOrder;

typedef struct requestPlaceMarketRepOrder {
	bool bypass_warning;
	char *position;
	double price;
	char* price_type;
	char* side;
	char* stop_condition;
	double stop_price;
	char *stop_symbol;
	char* symbol;
	char *validity_type;
	int volume;
} RequestPlaceMarketRepOrder;

typedef struct requestChangeMarketRepOrder {
	char* new_account_no;
	char* new_position;
	char* new_price_type;
	double new_price;
	int new_volume;
} RequestChangeMarketRepOrder;

typedef struct requestPlaceTradeReport {
	char* buyer;
	char* cpm;
	char* position;
	double price;
	char* seller;
	char* symbol;
	char* tr_type;
	int volume;
} RequestPlaceTradeReport;

typedef struct getOrderResponse {
	bool success;
	int status_code;
	Order data;
	char* message;
} GetOrderResponse;

typedef struct placeOrderResponse {
	bool success;
	int status_code;
	ResponsePlaceOrder data;
	char* message;
} PlaceOrderResponse;
/*
	End of Order Structs
*/

#endif
