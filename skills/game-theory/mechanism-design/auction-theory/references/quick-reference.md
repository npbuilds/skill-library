# Auction Theory — Quick Reference


## Single-Item Auctions

| Format | Rules | Winner | Payment |
|--------|-------|--------|---------|
| **English (ascending)** | Price rises; bidders drop out when price exceeds value | Last remaining bidder | Second-highest value (approximately) |
| **Dutch (descending)** | Price falls from high; first bidder to claim wins | First to stop the clock | Their bid (first-price) |
| **First-Price Sealed-Bid** | Submit sealed bids simultaneously; highest wins | Highest bidder | Their bid |
| **Second-Price Sealed-Bid (Vickrey)** | Submit sealed bids; highest wins, pays second-highest bid | Highest bidder | Second-highest bid |

## Real-World Auction Applications

| Application | Format | Scale | Key Design Feature |
|-------------|--------|-------|-------------------|
| FCC Spectrum Auctions | Simultaneous Multiple Round (SMR) / Combinatorial Clock | $60B+ since 1994 | Activity rules prevent bid sniping; package bidding handles complements |
| Online Ad Auctions (Google/Bing) | Generalized Second Price (GSP) | ~$200B/year globally | Position auctions; quality score adjustments; real-time bidding |
| Treasury Bond Auctions | Uniform-price or discriminatory | Trillions/year | Multiple units; strategic demand reduction |
| eBay | Proxy ascending (English variant) | Billions of transactions | Proxy bidding ≈ Vickrey; sniping as strategic response |
| Electricity Markets | Uniform-price with complex bids | Daily, regional | Start-up costs, ramping constraints, must-run status |
