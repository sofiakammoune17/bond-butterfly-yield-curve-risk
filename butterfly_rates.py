"""Bond butterfly with dated French TEC market yield proxies.

Run: python butterfly_rates.py
No external packages are required. Amounts are per 100 nominal.
"""
from dataclasses import dataclass
import csv
from pathlib import Path

SOURCE_URL = 'https://www.banque-france.fr/fr/statistiques/taux-et-cours/indices-obligataires-2026-09-24'
AS_OF = '2026-09-24'
TEC_23 = (3.496, 3.876, 4.477)
TEC_24 = (3.594, 4.049, 4.669)

@dataclass(frozen=True)
class Bond:
    label: str
    years: int
    coupon: float
    yield_rate: float

def price(b: Bond, y: float | None = None) -> float:
    rate = b.yield_rate if y is None else y
    return sum((100*b.coupon + (100 if t == b.years else 0))/(1+rate)**t
               for t in range(1,b.years+1))

def modified_duration(b: Bond) -> float:
    y=b.yield_rate
    derivative=sum(-t*(100*b.coupon+(100 if t==b.years else 0))/(1+y)**(t+1)
                   for t in range(1,b.years+1))
    return -derivative/price(b)

def pvbp(b: Bond) -> float:
    return price(b)*modified_duration(b)*0.0001

def solve_wings(bonds: list[Bond], belly_units: float = -1000.0) -> list[float]:
    a,m,z=bonds
    # Value neutrality and first-order parallel rate-risk neutrality.
    target_value=-belly_units*price(m)
    target_pvbp=-belly_units*pvbp(m)
    denominator=price(a)*pvbp(z)-price(z)*pvbp(a)
    if abs(denominator)<1e-12: raise ValueError('Cannot solve wings')
    q_a=(target_value*pvbp(z)-price(z)*target_pvbp)/denominator
    q_z=(price(a)*target_pvbp-target_value*pvbp(a))/denominator
    return [q_a,belly_units,q_z]

def scenario_pnl(bonds, quantities, shifts_bp):
    return sum(q*(price(b,b.yield_rate+shift/10000)-price(b))
               for b,q,shift in zip(bonds,quantities,shifts_bp))

def main():
    # CNO-TEC 24 Sep 2026 (Banque de France); coupon assumptions are illustrative.
    bonds=[Bond('2 ans',2,.035,TEC_24[0]/100),Bond('5 ans',5,.04,TEC_24[1]/100),Bond('10 ans',10,.045,TEC_24[2]/100)]
    quantities=solve_wings(bonds)
    cases={'Parallèle +50 pb':[50,50,50], 'Parallèle -50 pb':[-50,-50,-50],
           'Pentification':[-25,0,25], 'Courbure':[25,-50,25],
           'Amplitude 23-24 sept.':[round((now-prior)*100,1) for prior,now in zip(TEC_23,TEC_24)]}
    output = Path(__file__).with_name('resultats_scenarios.csv')
    with output.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['Scenario','Choc 2 ans (pb)','Choc 5 ans (pb)','Choc 10 ans (pb)','PnL pour 100 de nominal'])
        for name,shifts in cases.items(): w.writerow([name,*shifts,round(scenario_pnl(bonds,quantities,shifts),4)])
    print(f'Date des taux TEC : {AS_OF} | Source : {SOURCE_URL}')
    print('Coupons et obligations : hypotheses de modelisation ; TEC : taux publies.')
    print('Quantites 2/5/10 ans:',*[round(q,4) for q in quantities])
    print('Valeur nette:',round(sum(q*price(b) for q,b in zip(quantities,bonds)),8))
    print('PVBP net:',round(sum(q*pvbp(b) for q,b in zip(quantities,bonds)),8))
    for name,shifts in cases.items(): print(name,round(scenario_pnl(bonds,quantities,shifts),4))

if __name__=='__main__': main()
