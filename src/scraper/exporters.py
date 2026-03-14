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
        # Assuming your product dictionaries have a 'category' key
        cat = p.get('category', 'Unknown Category') 
        subcat = p.get('subcategory', 'Unknown Subcategory')
        
        # Use a tuple of (category, subcategory) as the dictionary key
        group_key = (cat, subcat)
        
        if group_key not in summary:
            summary[group_key] = {'total': 0, 'prices': [], 'missing_desc': 0}
        
        summary[group_key]['total'] += 1
        summary[group_key]['prices'].append(p['price'])
        if not p.get('description'):
            summary[group_key]['missing_desc'] += 1

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Category',              # Added Category header
            'Subcategory',
            'Total Products',
            'Avg Price',
            'Min Price',
            'Max Price',
            'Missing Descriptions',
            'Duplicates Removed (Global)'
        ])
        
        # Unpack the tuple key into cat and subcat
        for (cat, subcat), data in summary.items():
            prices = data['prices']
            avg_p = sum(prices) / len(prices) if prices else 0.0
            min_p = min(prices) if prices else 0.0
            max_p = max(prices) if prices else 0.0
            
            writer.writerow([
                cat,                 # Write the category first
                subcat,
                data['total'],
                round(avg_p, 2),
                min_p,
                max_p,
                data['missing_desc'],
                duplicates_removed
            ])