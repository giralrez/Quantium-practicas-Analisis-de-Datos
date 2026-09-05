#!/usr/bin/env python3
"""
Script para generar las visualizaciones faltantes del informe.
Ejecutar desde la carpeta raíz del proyecto: python scripts/generate_missing_plots.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuración de visualización
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette(['#1f77b4', '#2ca02c', '#d62728', '#ff7f0e', '#9467bd'])
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 11

def main():
    # Rutas
    base_path = Path(__file__).parent.parent
    output_dir = base_path / 'outputs' / 'visualizaciones'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Cargando datos...")
    df = pd.read_csv(base_path / 'QVI_data.csv')
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['YEARMONTH'] = df['DATE'].dt.year * 100 + df['DATE'].dt.month
    
    # Cargar datos de trial
    df2 = pd.read_csv(base_path / 'QVI_data_2.csv')
    df2['DATE'] = pd.to_datetime(df2['DATE'])
    df2['YEARMONTH'] = df2['DATE'].dt.year * 100 + df2['DATE'].dt.month
    
    # ============================================
    # 1. EVALUACIÓN DE TRIAL
    # ============================================
    print("Generando trial_evaluation.png...")
    
    tiendas_trial = {77: 233, 86: 155, 88: 237}
    
    fig, axes = plt.subplots(3, 2, figsize=(16, 14))
    fig.suptitle('Evaluación de Trial: Comparativa Tienda Prueba vs Control', 
                 fontsize=16, fontweight='bold')
    
    for idx, (trial, control) in enumerate(tiendas_trial.items()):
        # Calcular métricas
        trial_data = df2[df2['STORE_NBR'] == trial].groupby('YEARMONTH').agg(
            Ventas=('TOT_SALES', 'sum'),
            Clientes=('LYLTY_CARD_NBR', 'nunique')
        ).reset_index()
        
        control_data = df2[df2['STORE_NBR'] == control].groupby('YEARMONTH').agg(
            VentasControl=('TOT_SALES', 'sum'),
            ClientesControl=('LYLTY_CARD_NBR', 'nunique')
        ).reset_index()
        
        merged = trial_data.merge(control_data, on='YEARMONTH', how='inner')
        
        # Pre-trial scaling
        pre_trial = merged[merged['YEARMONTH'] < 201902]
        if len(pre_trial) > 0:
            scale_ventas = pre_trial['Ventas'].sum() / pre_trial['VentasControl'].sum()
            scale_clientes = pre_trial['Clientes'].sum() / pre_trial['ClientesControl'].sum()
        else:
            scale_ventas = scale_clientes = 1
        
        merged['VentasControlEsc'] = merged['VentasControl'] * scale_ventas
        merged['ClientesControlEsc'] = merged['ClientesControl'] * scale_clientes
        
        # Gráfico de ventas
        axes[idx, 0].plot(merged['YEARMONTH'], merged['Ventas'], marker='o',
                          linewidth=2, label=f'Tienda {trial}', color='#1f77b4')
        axes[idx, 0].plot(merged['YEARMONTH'], merged['VentasControlEsc'], marker='s',
                          linewidth=2, label=f'Control {control}', color='#d62728', linestyle='--')
        axes[idx, 0].axvspan(201902, 201904, alpha=0.2, color='gray', label='Periodo Trial')
        axes[idx, 0].set_title(f'Ventas - Tienda {trial}', fontsize=12)
        axes[idx, 0].set_ylabel('Ventas ($)', fontsize=10)
        axes[idx, 0].legend(fontsize=9)
        axes[idx, 0].grid(True, alpha=0.3)
        
        # Gráfico de clientes
        axes[idx, 1].plot(merged['YEARMONTH'], merged['Clientes'], marker='o',
                          linewidth=2, label=f'Tienda {trial}', color='#2ca02c')
        axes[idx, 1].plot(merged['YEARMONTH'], merged['ClientesControlEsc'], marker='s',
                          linewidth=2, label=f'Control {control}', color='#d62728', linestyle='--')
        axes[idx, 1].axvspan(201902, 201904, alpha=0.2, color='gray', label='Periodo Trial')
        axes[idx, 1].set_title(f'Clientes - Tienda {trial}', fontsize=12)
        axes[idx, 1].set_ylabel('Clientes Únicos', fontsize=10)
        axes[idx, 1].legend(fontsize=9)
        axes[idx, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'trial_evaluation.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("  [OK] trial_evaluation.png generado")
    
    # ============================================
    # 2. CONCLUSIONES
    # ============================================
    print("Generando conclusiones.png...")
    
    # Calcular KPIs
    total_ventas = df['TOT_SALES'].sum()
    total_unidades = df['PROD_QTY'].sum()
    total_clientes = df['LYLTY_CARD_NBR'].nunique()
    ticket_promedio = total_ventas / df['TXN_ID'].nunique()
    
    # Top segmentos
    segmentos = df.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER']).agg(
        Ventas=('TOT_SALES', 'sum')
    ).reset_index()
    segmentos['Participacion'] = segmentos['Ventas'] / segmentos['Ventas'].sum() * 100
    top3 = segmentos.sort_values('Ventas', ascending=False).head(3)
    
    # Top marcas
    marcas_share = (df.groupby('BRAND')['TOT_SALES'].sum() / df['TOT_SALES'].sum() * 100).sort_values(ascending=False).head(5)
    
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.axis('off')
    
    titulo = 'CONCLUSIONES EJECUTIVAS - ANÁLISIS DE CATEGORÍA CHIPS'
    ax.text(0.5, 0.95, titulo, fontsize=16, fontweight='bold', ha='center', va='top',
            transform=ax.transAxes)
    
    conclusiones = [
        ('KPIs GENERALES', [
            f'Ventas totales: ${total_ventas:,.0f}',
            f'Unidades vendidas: {total_unidades:,.0f}',
            f'Clientes únicos: {total_clientes:,}',
            f'Ticket promedio: ${ticket_promedio:.2f}'
        ]),
        ('SEGMENTOS DE MAYOR VALOR', [
            f'{row["LIFESTAGE"]} - {row["PREMIUM_CUSTOMER"]}: ${row["Ventas"]:,.0f} ({row["Participacion"]:.1f}%)'
            for _, row in top3.iterrows()
        ]),
        ('MARCAS LÍDERES', [
            f'{marca}: {share:.1f}% de participación'
            for marca, share in marcas_share.items()
        ]),
        ('EVALUACIÓN DE TRIAL', [
            'Tienda 77: Incremento significativo en VENTAS',
            'Tienda 86: Incremento significativo en CLIENTES',
            'Tienda 88: Incremento significativo en AMBAS métricas'
        ]),
        ('RECOMENDACIONES', [
            'Priorizar marcas premium en segmentos Mainstream',
            'Enfocar surtido en empaques grandes (270g-380g)',
            'Mantener precios premium donde hay disposición a pagar',
            'Continuar rollout del exitoso trial'
        ])
    ]
    
    y_pos = 0.88
    for titulo_seccion, items in conclusiones:
        ax.text(0.05, y_pos, titulo_seccion, fontsize=12, fontweight='bold',
                transform=ax.transAxes, color='#1f77b4')
        y_pos -= 0.03
        for item in items:
            ax.text(0.08, y_pos, f'• {item}', fontsize=10, transform=ax.transAxes)
            y_pos -= 0.025
        y_pos -= 0.02
    
    plt.tight_layout()
    plt.savefig(output_dir / 'conclusiones.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("  [OK] conclusiones.png generado")
    
    # ============================================
    # RESUMEN
    # ============================================
    print("\n" + "="*50)
    print("VISUALIZACIONES GENERADAS:")
    print("="*50)
    for file in sorted(output_dir.glob('*.png')):
        size_kb = file.stat().st_size / 1024
        print(f"  {file.name:<30} {size_kb:>8.1f} KB")
    print("="*50)
    print(f"\nTotal: {len(list(output_dir.glob('*.png')))} archivos PNG")

if __name__ == '__main__':
    main()
