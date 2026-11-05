# -*- coding: utf-8 -*-
"""Export de diagnostiques en PDF pour rapports professionnels"""

from datetime import datetime
import json
from app.models.diagnostic import Diagnostic

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("⚠️ reportlab not installed. Install with: pip install reportlab")


def generate_diagnostic_pdf(diagnostic: Diagnostic, output_path: str = None) -> str:
    """
    Génère un rapport PDF professionnel pour un diagnostic
    
    Args:
        diagnostic: Diagnostic object from DB
        output_path: Chemin de sortie (defaut: /tmp/diagnostic_{id}_{timestamp}.pdf)
    
    Returns:
        Chemin du fichier PDF généré
    """
    
    if not REPORTLAB_AVAILABLE:
        raise ImportError("reportlab required for PDF export. Install with: pip install reportlab")
    
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"/tmp/diagnostic_{diagnostic.id}_{timestamp}.pdf"
    
    # Configuration du PDF
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Styles personnalisés
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#2E7D32'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#1565C0'),
        spaceAfter=6,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_LEFT,
        spaceAfter=6
    )
    
    # En-tête
    story.append(Paragraph("📋 RAPPORT DE DIAGNOSTIC AGRICOLE", title_style))
    story.append(Paragraph(f"AgroNavig - Diagnostic IA pour Agriculture Durable", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Informations générales
    story.append(Paragraph("INFORMATIONS GÉNÉRALES", heading_style))
    general_data = [
        ["Diagnostic ID", str(diagnostic.id)],
        ["Date du Diagnostic", str(diagnostic.created_at)],
        ["Culture Analysée", diagnostic.culture],
        ["Utilisateur ID", str(diagnostic.user_id)],
    ]
    general_table = Table(general_data, colWidths=[2*inch, 3*inch])
    general_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8F5E9')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(general_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Résultats du diagnostic
    story.append(Paragraph("RÉSULTATS DE L'ANALYSE", heading_style))
    
    # Déterminer couleur du niveau
    niveau_colors = {
        "sain": colors.HexColor('#4CAF50'),
        "faible": colors.HexColor('#FFC107'),
        "moyen": colors.HexColor('#FF9800'),
        "élevé": colors.HexColor('#F44336'),
        "inconnu": colors.HexColor('#9E9E9E'),
    }
    
    result_data = [
        ["Maladie Identifiée", diagnostic.maladie],
        ["Niveau de Gravité", diagnostic.niveau.upper()],
        ["Confiance IA", f"{diagnostic.confiance}%"],
        ["Classe Prédite", diagnostic.maladie],
    ]
    
    # Ajouter confiance ajustée si disponible
    if diagnostic.metadata:
        metadata = json.loads(diagnostic.metadata)
        if "confidence_adjusted" in metadata:
            result_data.append(["Confiance Ajustée (contexte)", f"{metadata['confidence_adjusted']}%"])
        if "season" in metadata:
            result_data.append(["Saison Actuelle", metadata['season']])
    
    result_table = Table(result_data, colWidths=[2*inch, 3*inch])
    result_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E3F2FD')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(result_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Top 3 prédictions si disponibles
    if diagnostic.top_predictions:
        story.append(Paragraph("ANALYSE MULTICRITÈRE (Top 3 Prédictions)", heading_style))
        try:
            top_3 = json.loads(diagnostic.top_predictions)
            top_3_data = [["Rang", "Maladie", "Confiance"]]
            for idx, pred in enumerate(top_3[:3], 1):
                top_3_data.append([
                    str(idx),
                    pred.get("classe", "Unknown"),
                    f"{pred.get('score', 0):.1f}%"
                ])
            top_3_table = Table(top_3_data, colWidths=[1*inch, 3*inch, 1.5*inch])
            top_3_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#CFD8DC')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ]))
            story.append(top_3_table)
            story.append(Spacer(1, 0.2*inch))
        except Exception as e:
            print(f"Erreur chargement top_predictions: {e}")
    
    # Description/Symptômes
    if diagnostic.description:
        story.append(Paragraph("DESCRIPTION & SYMPTÔMES", heading_style))
        story.append(Paragraph(diagnostic.description, body_style))
        story.append(Spacer(1, 0.1*inch))
    
    # Traitement/Recommandations
    if diagnostic.traitement:
        story.append(Paragraph("TRAITEMENT RECOMMANDÉ", heading_style))
        try:
            traitements = json.loads(diagnostic.traitement) if isinstance(diagnostic.traitement, str) else diagnostic.traitement
            if isinstance(traitements, list):
                for i, traitement in enumerate(traitements, 1):
                    if isinstance(traitement, dict):
                        story.append(Paragraph(f"<b>{i}. {traitement.get('nom', 'Traitement')}:</b> {traitement.get('description', '')}", body_style))
                    else:
                        story.append(Paragraph(f"<b>{i}.</b> {traitement}", body_style))
            else:
                story.append(Paragraph(str(traitements), body_style))
        except Exception as e:
            story.append(Paragraph(str(diagnostic.traitement), body_style))
        
        story.append(Spacer(1, 0.1*inch))
    
    # Recommandations contextuelles
    if diagnostic.metadata:
        try:
            metadata = json.loads(diagnostic.metadata)
            if "seasonal_recommendations" in metadata and metadata["seasonal_recommendations"]:
                story.append(Paragraph("RECOMMANDATIONS SAISONNIÈRES", heading_style))
                for rec in metadata["seasonal_recommendations"]:
                    story.append(Paragraph(f"• {rec}", body_style))
                story.append(Spacer(1, 0.1*inch))
        except Exception as e:
            print(f"Erreur chargement metadata: {e}")
    
    # Statut de validation
    if diagnostic.validated_by_user:
        story.append(Paragraph("VALIDATION UTILISATEUR", heading_style))
        if diagnostic.user_feedback:
            try:
                feedback = json.loads(diagnostic.user_feedback)
                story.append(Paragraph(f"<b>Statut:</b> {feedback.get('status', 'unknown').upper()}", body_style))
                if feedback.get('comment'):
                    story.append(Paragraph(f"<b>Commentaire:</b> {feedback.get('comment')}", body_style))
            except:
                story.append(Paragraph("Diagnostique validé par l'utilisateur", body_style))
    
    # Pied de page
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(
        "Ce rapport a été généré automatiquement par AgroNavig. "
        "Les résultats doivent être vérifiés par un expert agronomique avant application.",
        styles['Normal']
    ))
    
    # Générer le PDF
    doc.build(story)
    print(f"✅ PDF généré: {output_path}")
    return output_path


def generate_batch_diagnostics_pdf(diagnostics: list, output_path: str = None) -> str:
    """
    Génère un rapport PDF regroupant plusieurs diagnostiques
    
    Args:
        diagnostics: Liste d'objets Diagnostic
        output_path: Chemin de sortie
    
    Returns:
        Chemin du fichier PDF généré
    """
    
    if not REPORTLAB_AVAILABLE:
        raise ImportError("reportlab required for PDF export. Install with: pip install reportlab")
    
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"/tmp/diagnostics_batch_{timestamp}.pdf"
    
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#2E7D32'),
        alignment=TA_CENTER,
    )
    
    # En-tête
    story.append(Paragraph("📊 RAPPORT BATCH DE DIAGNOSTIQUES", title_style))
    story.append(Paragraph(f"Nombre total: {len(diagnostics)} | Généré: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Tableau récapitulatif
    summary_data = [["ID", "Culture", "Maladie", "Confiance", "Niveau", "Date"]]
    for diag in diagnostics[:20]:  # Limiter à 20 pour la lisibilité
        summary_data.append([
            str(diag.id),
            diag.culture,
            diag.maladie,
            f"{diag.confiance}%",
            diag.niveau,
            diag.created_at.strftime("%d/%m/%Y")
        ])
    
    summary_table = Table(summary_data, colWidths=[0.6*inch, 1.2*inch, 1.5*inch, 1*inch, 0.8*inch, 1*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#CFD8DC')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(summary_table)
    
    # Statistiques
    story.append(Spacer(1, 0.2*inch))
    avg_conf = sum(d.confiance for d in diagnostics) / len(diagnostics) if diagnostics else 0
    unique_diseases = len(set(d.maladie for d in diagnostics))
    
    story.append(Paragraph(f"<b>Statistiques Globales:</b>", styles['Normal']))
    story.append(Paragraph(f"• Confiance moyenne: {avg_conf:.1f}%", styles['Normal']))
    story.append(Paragraph(f"• Maladies uniques identifiées: {unique_diseases}", styles['Normal']))
    
    doc.build(story)
    print(f"✅ Batch PDF généré: {output_path}")
    return output_path
