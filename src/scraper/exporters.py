import csv
import os

def export_products(products, filepath):
    """Export products to CSV file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not products:
        return

    keys = products[0].keys()
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(products)

def export_summary(products, filepath, duplicates_removed):
    """Export category summary report to CSV file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    summary = {}
    for p in products:
        subcat = p['subcategory']
        if subcat not in summary:
            summary[subcat] = {'total': 0, 'prices': [], 'missing_desc': 0}
        
        summary[subcat]['total'] += 1
        summary[subcat]['prices'].append(p['price'])
        if not p['description']:
            summary[subcat]['missing_desc'] += 1

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Subcategory',
            'Total Products',
            'Avg Price',
            'Min Price',
            'Max Price',
            'Missing Descriptions',
            'Duplicates Removed (Global)'
        ])
        
        for subcat, data in summary.items():
            prices = data['prices']
            avg_p = sum(prices) / len(prices) if prices else 0.0
            min_p = min(prices) if prices else 0.0
            max_p = max(prices) if prices else 0.0
            
            writer.writerow([
                subcat,
                data['total'],
                round(avg_p, 2),
                min_p,
                max_p,
                data['missing_desc'],
                duplicates_removed
            ])
