class BarProgress:
    @staticmethod
    def create(current: int, total: int, barBlock: int = 30):
        fillBlock = "█";
        emptyBlock = "░";
        barProgress = '';

        if current == 0 & total == 0: 
            total = current = 1;
    
        if current > total: current = total;
    
        porcent = (current * 100) / total;
        filledBlocksNeeded = (porcent / 100) * barBlock;
    
        barProgress += fillBlock * int(filledBlocksNeeded)
        barProgress += emptyBlock * int(barBlock - filledBlocksNeeded)
    
        return barProgress