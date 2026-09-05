#!/usr/bin/env python3
"""
Script para exportar métricas procesadas de Quantium en formato CSV para Power BI.
Lee QVI_data.csv y genera 7 archivos CSV con métricas calculadas.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys


def load_data(file_path: str) -> pd.DataFrame:
    """Carga y prepara los datos base."""
    df = pd.read_csv(file_path)
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['YEARMONTH'] = df['DATE'].dt.year * 100 + df['DATE'].dt.month
    return df


def calculate_kpis_resumen(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula KPIs globales resumen."""
    kpis = pd.DataFrame({
        'Metrica': [
            'Ventas Totales ($)',
            'Unidades Totales',
            'Clientes Únicos',
            'Transacciones Totales',
            'Ticket Promedio ($)',
            'Precio Promedio por Unidad ($)',
            'Frecuencia Promedio (transacciones/cliente)',
            'Chips Promedio por Transacción'
        ],
        'Valor': [
            df['TOT_SALES'].sum(),
            df['PROD_QTY'].sum(),
            df['LYLTY_CARD_NBR'].nunique(),
            df['TXN_ID'].nunique(),
            df['TOT_SALES'].sum() / df['TXN_ID'].nunique(),
            df['TOT_SALES'].sum() / df['PROD_QTY'].sum(),
            df['TXN_ID'].nunique() / df['LYLTY_CARD_NBR'].nunique(),
            df['PROD_QTY'].sum() / df['TXN_ID'].nunique()
        ],
        'Descripcion': [
            'Suma de todas las ventas en el período',
            'Total de unidades de chips vendidas',
            'Número de clientes únicos con tarjeta de fidelidad',
            'Número total de transacciones realizadas',
            'Promedio de gasto por transacción',
            'Precio promedio por unidad de chip',
            'Promedio de transacciones por cliente',
            'Promedio de unidades por transacción'
        ]
    })
    return kpis


def calculate_metricas_mensuales(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula métricas mensuales por tienda."""
    monthly = df.groupby(['STORE_NBR', 'YEARMONTH']).agg(
        Ventas=('TOT_SALES', 'sum'),
        Unidades=('PROD_QTY', 'sum'),
        Clientes=('LYLTY_CARD_NBR', 'nunique'),
        Transacciones=('TXN_ID', 'nunique')
    ).reset_index()
    
    monthly['Frecuencia'] = monthly['Transacciones'] / monthly['Clientes']
    monthly['ChipsPorTransaccion'] = monthly['Unidades'] / monthly['Transacciones']
    monthly['PrecioPromedio'] = monthly['Ventas'] / monthly['Unidades']
    
    # Agregar fecha legible
    monthly['Fecha'] = pd.to_datetime(monthly['YEARMONTH'].astype(str), format='%Y%m')
    
    return monthly


def calculate_ventas_por_segmento(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula métricas por segmento de cliente (LIFESTAGE × PREMIUM_CUSTOMER)."""
    segmentos = df.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER']).agg(
        Ventas=('TOT_SALES', 'sum'),
        Unidades=('PROD_QTY', 'sum'),
        Clientes=('LYLTY_CARD_NBR', 'nunique'),
        Transacciones=('TXN_ID', 'nunique')
    ).reset_index()
    
    segmentos['TicketPromedio'] = segmentos['Ventas'] / segmentos['Transacciones']
    segmentos['Frecuencia'] = segmentos['Transacciones'] / segmentos['Clientes']
    segmentos['PrecioPromedio'] = segmentos['Ventas'] / segmentos['Unidades']
    segmentos['ParticipacionVentas'] = segmentos['Ventas'] / segmentos['Ventas'].sum() * 100
    
    return segmentos


def calculate_afinidad_marcas(df: pd.DataFrame, segmento_objetivo: dict = None) -> pd.DataFrame:
    """Calcula índice de afinidad por marca para un segmento específico."""
    if segmento_objetivo is None:
        # Segmento por defecto: Mainstream Young Singles/Couples
        segmento_objetivo = {
            'LIFESTAGE': 'YOUNG SINGLES/COUPLES',
            'PREMIUM_CUSTOMER': 'Mainstream'
        }
    
    # Filtrar segmento objetivo
    mask_objetivo = pd.Series(True, index=df.index)
    for col, val in segmento_objetivo.items():
        mask_objetivo &= (df[col] == val)
    
    target = df[mask_objetivo]
    rest = df[~mask_objetivo]
    
    # Calcular proporciones
    target_brand_share = target['BRAND'].value_counts(normalize=True)
    rest_brand_share = rest['BRAND'].value_counts(normalize=True)
    
    # Evitar división por cero
    rest_brand_share = rest_brand_share.replace(0, np.nan)
    
    # Índice de afinidad
    affinity = (target_brand_share / rest_brand_share).sort_values(ascending=False)
    
    # Calcular ventas absolutas
    ventas_abs = target.groupby('BRAND')['TOT_SALES'].sum()
    
    result = pd.DataFrame({
        'BRAND': affinity.index,
        'IndiceAfinidad': affinity.values,
        'VentasAbsolutas': ventas_abs.reindex(affinity.index).values,
        'ParticipacionPorcentual': (target_brand_share.reindex(affinity.index).values * 100)
    })
    
    return result


def calculate_afinidad_paquetes(df: pd.DataFrame, segmento_objetivo: dict = None) -> pd.DataFrame:
    """Calcula índice de afinidad por tamaño de paquete."""
    if segmento_objetivo is None:
        segmento_objetivo = {
            'LIFESTAGE': 'YOUNG SINGLES/COUPLES',
            'PREMIUM_CUSTOMER': 'Mainstream'
        }
    
    mask_objetivo = pd.Series(True, index=df.index)
    for col, val in segmento_objetivo.items():
        mask_objetivo &= (df[col] == val)
    
    target = df[mask_objetivo]
    rest = df[~mask_objetivo]
    
    target_pack_share = target['PACK_SIZE'].value_counts(normalize=True)
    rest_pack_share = rest['PACK_SIZE'].value_counts(normalize=True)
    
    rest_pack_share = rest_pack_share.replace(0, np.nan)
    
    affinity = (target_pack_share / rest_pack_share).sort_values(ascending=False)
    ventas_abs = target.groupby('PACK_SIZE')['TOT_SALES'].sum()
    
    result = pd.DataFrame({
        'PACK_SIZE': affinity.index,
        'IndiceAfinidad': affinity.values,
        'VentasAbsolutas': ventas_abs.reindex(affinity.index).values,
        'ParticipacionPorcentual': (target_pack_share.reindex(affinity.index).values * 100)
    })
    
    return result


def calculate_tendencia_mensual(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula tendencia mensual agregada (todas las tiendas)."""
    tendencia = df.groupby('YEARMONTH').agg(
        Ventas=('TOT_SALES', 'sum'),
        Unidades=('PROD_QTY', 'sum'),
        Clientes=('LYLTY_CARD_NBR', 'nunique'),
        Transacciones=('TXN_ID', 'nunique')
    ).reset_index()
    
    tendencia['Fecha'] = pd.to_datetime(tendencia['YEARMONTH'].astype(str), format='%Y%m')
    tendencia['TicketPromedio'] = tendencia['Ventas'] / tendencia['Transacciones']
    
    return tendencia


def calculate_evaluacion_trial(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula métricas de evaluación para las tiendas de prueba (77, 86, 88)."""
    # Definir tiendas de prueba y sus controles (del notebook Task2)
    tiendas_trial = {
        77: 233,
        86: 155,
        88: 237
    }
    
    resultados = []
    
    for trial_store, control_store in tiendas_trial.items():
        # Filtrar datos para cada tienda
        trial_data = df[df['STORE_NBR'] == trial_store]
        control_data = df[df['STORE_NBR'] == control_store]
        
        # Calcular métricas mensuales para cada tienda
        trial_monthly = trial_data.groupby('YEARMONTH').agg(
            VentasTrial=('TOT_SALES', 'sum'),
            ClientesTrial=('LYLTY_CARD_NBR', 'nunique')
        ).reset_index()
        
        control_monthly = control_data.groupby('YEARMONTH').agg(
            VentasControl=('TOT_SALES', 'sum'),
            ClientesControl=('LYLTY_CARD_NBR', 'nunique')
        ).reset_index()
        
        # Unir datos
        merged = trial_monthly.merge(control_monthly, on='YEARMONTH', how='inner')
        
        # Calcular factores de escala (pre-trial)
        pre_trial = merged[merged['YEARMONTH'] < 201902]
        if len(pre_trial) > 0:
            scaling_ventas = pre_trial['VentasTrial'].sum() / pre_trial['VentasControl'].sum()
            scaling_clientes = pre_trial['ClientesTrial'].sum() / pre_trial['ClientesControl'].sum()
        else:
            scaling_ventas = 1
            scaling_clientes = 1
        
        # Aplicar escala y calcular diferencias
        merged['VentasControlEscalada'] = merged['VentasControl'] * scaling_ventas
        merged['ClientesControlEscalada'] = merged['ClientesControl'] * scaling_clientes
        
        merged['PorcentajeDiffVentas'] = abs(merged['VentasControlEscalada'] - merged['VentasTrial']) / merged['VentasControlEscalada']
        merged['PorcentajeDiffClientes'] = abs(merged['ClientesControlEscalada'] - merged['ClientesTrial']) / merged['ClientesControlEscalada']
        
        # Calcular t-values (usando desviación estándar pre-trial)
        std_ventas = pre_trial['PorcentajeDiffVentas'].std(ddof=1) if len(pre_trial) > 1 else 0
        std_clientes = pre_trial['PorcentajeDiffClientes'].std(ddof=1) if len(pre_trial) > 1 else 0
        
        merged['tValueVentas'] = merged['PorcentajeDiffVentas'] / std_ventas if std_ventas > 0 else 0
        merged['tValueClientes'] = merged['PorcentajeDiffClientes'] / std_clientes if std_clientes > 0 else 0
        
        # Determinar significancia (t > 1.895 para 95% confianza, 7 gl)
        merged['SignificativoVentas'] = merged['tValueVentas'] > 1.895
        merged['SignificativoClientes'] = merged['tValueClientes'] > 1.895
        
        # Agregar info de tiendas
        merged['TiendaPrueba'] = trial_store
        merged['TiendaControl'] = control_store
        
        # Filtrar solo meses del trial (feb-abr 2019)
        trial_months = merged[(merged['YEARMONTH'] >= 201902) & (merged['YEARMONTH'] <= 201904)]
        
        resultados.append(trial_months)
    
    return pd.concat(resultados, ignore_index=True)


def main():
    """Función principal que ejecuta todas las exportaciones."""
    # Configurar rutas
    base_path = Path(__file__).parent.parent
    data_file = base_path / 'data' / 'raw' / 'QVI_data.csv'
    output_dir = base_path / 'outputs' / 'csv_powerbi'
    
    # Crear directorio de salida si no existe
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Cargando datos...")
    df = load_data(data_file)
    print(f"Datos cargados: {len(df)} registros")
    
    # 1. KPIs Resumen
    print("Calculando KPIs resumen...")
    kpis = calculate_kpis_resumen(df)
    kpis.to_csv(output_dir / 'kpis_resumen.csv', index=False, encoding='utf-8-sig')
    
    # 2. Métricas Mensuales
    print("Calculando métricas mensuales...")
    mensuales = calculate_metricas_mensuales(df)
    mensuales.to_csv(output_dir / 'metricas_mensuales.csv', index=False, encoding='utf-8-sig')
    
    # 3. Ventas por Segmento
    print("Calculando ventas por segmento...")
    segmentos = calculate_ventas_por_segmento(df)
    segmentos.to_csv(output_dir / 'ventas_por_segmento.csv', index=False, encoding='utf-8-sig')
    
    # 4. Afinidad de Marcas
    print("Calculando afinidad de marcas...")
    afinidad_marcas = calculate_afinidad_marcas(df)
    afinidad_marcas.to_csv(output_dir / 'afinidad_marcas.csv', index=False, encoding='utf-8-sig')
    
    # 5. Afinidad de Paquetes
    print("Calculando afinidad de paquetes...")
    afinidad_paquetes = calculate_afinidad_paquetes(df)
    afinidad_paquetes.to_csv(output_dir / 'afinidad_paquetes.csv', index=False, encoding='utf-8-sig')
    
    # 6. Tendencia Mensual
    print("Calculando tendencia mensual...")
    tendencia = calculate_tendencia_mensual(df)
    tendencia.to_csv(output_dir / 'tendencia_mensual.csv', index=False, encoding='utf-8-sig')
    
    # 7. Evaluación de Trial
    print("Calculando evaluación de trial...")
    # Usar QVI_data_2.csv para evaluación de trial (tiene más información)
    data2_file = base_path / 'data' / 'raw' / 'QVI_data_2.csv'
    if data2_file.exists():
        df2 = pd.read_csv(data2_file)
        df2['DATE'] = pd.to_datetime(df2['DATE'])
        df2['YEARMONTH'] = df2['DATE'].dt.year * 100 + df2['DATE'].dt.month
        trial_eval = calculate_evaluacion_trial(df2)
    else:
        trial_eval = calculate_evaluacion_trial(df)
    trial_eval.to_csv(output_dir / 'evaluacion_trial.csv', index=False, encoding='utf-8-sig')
    
    print(f"\n¡Exportación completada!")
    print(f"Archivos CSV generados en: {output_dir}")
    print("\nArchivos generados:")
    for file in sorted(output_dir.glob('*.csv')):
        print(f"  - {file.name}")


if __name__ == '__main__':
    main()
