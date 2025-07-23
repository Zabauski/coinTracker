from textual.app import App, ComposeResult
from textual.widgets import DataTable 
from rich.text import Text
from colorama import Fore, Style, init
from prices import get_coin_price , highlight_letter
from portfolio import portfolio  







class CoinPortfolioTable(App):
    
    sort_directions = {}
 
    CSS_PATH = "style.css"
   
    init()

    

   
    def compose(self) -> ComposeResult:

        
      
        
       


        table = DataTable(id="coin_table",)
       # table.add_columns("Procent,%", "Coin", "Price,$", "Amount", "Value,$", "Invested,$", "PnL,%")     
       

        procG = Text("procent,%")
        procG.stylize("green", 0, 1)
        table.add_column(procG,key="procent", width=10)

        
        coinG = Text("coin")
        coinG.stylize("green", 0, 1)
        table.add_column(coinG,key="coin", width=10)

        priceG = Text("price,$")
        priceG.stylize("green",1, 2)
        table.add_column(priceG,key="price", width=10)
        amauntG = Text("amount")
        amauntG.stylize("green",0, 1)
        table.add_column(amauntG,key="amount", width=12)
        valueG = Text("value,$")
        valueG.stylize("green",0, 1)
        table.add_column(valueG,key="value", width=10)
        investG = Text("invested,$")
        investG.stylize("green",0, 1)
        table.add_column(investG,key="invested", width=12)
        pnlG = Text("pnl,%")
        pnlG.stylize("green",2, 3)
        table.add_column(pnlG,key="pnl", width=5)
        table.add_column("", width=1)

        table.zebra_stripes = True
        table.show_cursor = False 
        yield table

        total = DataTable(id="total_table")
#        total.add_columns("                                        ", "Value,$", "Invested,$", "PnL,%")  
        total.add_column("",width=48)
        total.add_column("Value,$", width=10)
        total.add_column("Invested,$", width=12)
        total.add_column("PnL,%", width=5)
        total.add_column("", width=1)

        total.show_cursor = False 
        yield total
        

    def on_mount(self):
        self.update_tables()
        self.set_interval(60, self.update_tables) 

    def update_tables(self):
        table = self.query_one("#coin_table", DataTable)
        total_table = self.query_one("#total_table", DataTable)
        
        table.clear()
        total_table.clear()

        coin_symbols = [coin["symbol"] for coin in portfolio]
        coins_price = get_coin_price(coin_symbols)

        total_value = sum(coins_price.get(coin["symbol"], {}).get("usd", 0) * coin["amount"] for coin in portfolio) 
        total_invested = sum(coin["invested"] for coin in portfolio)
        

        for coin in portfolio:
            price = coins_price.get(coin["symbol"], {}).get("usd", 0)
            amount = coin["amount"]
            invested = coin["invested"]
            value = price * amount
            pnl = ((value - invested) / (invested if invested != 0 else 1)) * 100
            if pnl < 0 :
                triangle = Text("▼", style="bold red")
            else :
                triangle = triangle = Text("▲", style="bold green") 
            procent = (100 *  value ) / total_value
            
            table.add_row(
                f"{procent:.0f} ",
                coin["name"],
                f"{price:.2f}",
                f"{amount:.2f}",
                f"{value:.2f}",
                f"{invested:.2f}",
                f"{pnl:.2f}",
                triangle
            )

        overall_pnl = ((total_value - total_invested) / total_invested) * 100 
        if overall_pnl < 0 :
            overall_triangle = Text("▼", style="bold red")
        else :
            overall_triangle = triangle = Text("▲", style="bold green") 
        

        total_table = self.query_one("#total_table", DataTable)
        
        total_table.add_row(
            "",
            f"{total_value:.2f}",
            f"{total_invested:.2f}",
            f"{overall_pnl:.2f}",
            overall_triangle
            
        )

    def sort_reverse(self, column_key: str) -> bool:  
        self.sort_directions[column_key] = not self.sort_directions.get(column_key, False)
        return self.sort_directions[column_key]

    def action_sort_by_coin_name(self) -> None :
        table = self.query_one(DataTable)
        table.sort(
            "coin",  
            key=lambda row:row,  
            reverse=self.sort_reverse("procent"),  
        )

    def action_sort_by_procent(self) -> None :
        table = self.query_one(DataTable)
        table.sort(
            "procent",  
            key=lambda row: float(row),  
            reverse=self.sort_reverse("procent"),  
        )




    def action_sort_by_price(self) -> None :
        table = self.query_one(DataTable)
        table.sort(
            "price",  
            key=lambda row: float(row),  
            reverse=self.sort_reverse("procent"),  
        )
    def action_sort_by_amount(self) -> None :
        table = self.query_one(DataTable)
        table.sort(
            "amount",  
            key=lambda row: float(row),  
            reverse=self.sort_reverse("procent"),  
        )
    def action_sort_by_value(self) -> None :
        table = self.query_one(DataTable)
        table.sort(
            "value",  
            key=lambda row: float(row),  
            reverse=self.sort_reverse("procent"),  
        )
    def action_sort_by_invested(self) -> None :
        table = self.query_one(DataTable)
        table.sort(
            "invested",  
            key=lambda row: float(row),  
            reverse=self.sort_reverse("procent"),  
        )
    def action_sort_by_pnl(self) -> None :
        table = self.query_one(DataTable)
        table.sort(
            "pnl",  
            key=lambda row: float(row),  
            reverse=self.sort_reverse("pnl"),  
        )

   
    def on_key(self, event):
        key = event.key.lower()
    
        if key == "q":
            self.exit()
        elif key == "p":
            self.action_sort_by_procent()
        elif key == "c":
            self.action_sort_by_coin_name()
        elif key == "r":
            self.action_sort_by_price()
        elif key == "a":
            self.action_sort_by_amount()  # Обратите внимание на отступ
        elif key == "v":
            self.action_sort_by_value()
        elif key == "i":
            self.action_sort_by_invested()
        elif key == "l":
            self.action_sort_by_pnl()





CoinPortfolioTable().run()




