//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.10.05 alle 12:50:22 PM CEST 
//


package cnr.isti.sse.big.data.transazioni;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.adapters.CollapsedStringAdapter;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;


/**
 * <p>Classe Java per anonymous complex type.
 * 
 * <p>Il seguente frammento di schema specifica il contenuto previsto contenuto in questa classe.
 * 
 * <pre>
 * &lt;complexType>
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element ref="{}CodiceAbbonamento"/>
 *         &lt;element ref="{}ProgressivoAbbonamento"/>
 *         &lt;element ref="{}Turno"/>
 *         &lt;element ref="{}QuantitaEventiAbilitati"/>
 *         &lt;element ref="{}Validita"/>
 *         &lt;element ref="{}Rateo"/>
 *         &lt;element ref="{}RateoIntrattenimenti"/>
 *         &lt;element ref="{}RateoIVA"/>
 *         &lt;element ref="{}CorrispettivoLordo" minOccurs="0"/>
 *         &lt;element ref="{}Prevendita" minOccurs="0"/>
 *         &lt;element ref="{}IVACorrispettivo" minOccurs="0"/>
 *         &lt;element ref="{}IVAPrevendita" minOccurs="0"/>
 *         &lt;element ref="{}ImportoFigurativo" minOccurs="0"/>
 *         &lt;element ref="{}IVAFigurativa" minOccurs="0"/>
 *         &lt;element ref="{}Partecipante" minOccurs="0"/>
 *       &lt;/sequence>
 *       &lt;attribute name="Annullamento" default="N">
 *         &lt;simpleType>
 *           &lt;restriction base="{http://www.w3.org/2001/XMLSchema}NMTOKEN">
 *             &lt;enumeration value="S"/>
 *             &lt;enumeration value="N"/>
 *           &lt;/restriction>
 *         &lt;/simpleType>
 *       &lt;/attribute>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "codiceAbbonamento",
    "progressivoAbbonamento",
    "turno",
    "quantitaEventiAbilitati",
    "validita",
    "rateo",
    "rateoIntrattenimenti",
    "rateoIVA",
    "corrispettivoLordo",
    "prevendita",
    "ivaCorrispettivo",
    "ivaPrevendita",
    "importoFigurativo",
    "ivaFigurativa",
    "partecipante"
})
@XmlRootElement(name = "Abbonamento")
public class Abbonamento {

    @XmlElement(name = "CodiceAbbonamento", required = true)
    protected String codiceAbbonamento;
    @XmlElement(name = "ProgressivoAbbonamento", required = true)
    protected String progressivoAbbonamento;
    @XmlElement(name = "Turno", required = true)
    protected Turno turno;
    @XmlElement(name = "QuantitaEventiAbilitati", required = true)
    protected String quantitaEventiAbilitati;
    @XmlElement(name = "Validita", required = true)
    protected String validita;
    @XmlElement(name = "Rateo", required = true)
    protected String rateo;
    @XmlElement(name = "RateoIntrattenimenti", required = true)
    protected String rateoIntrattenimenti;
    @XmlElement(name = "RateoIVA", required = true)
    protected String rateoIVA;
    @XmlElement(name = "CorrispettivoLordo")
    protected String corrispettivoLordo;
    @XmlElement(name = "Prevendita")
    protected String prevendita;
    @XmlElement(name = "IVACorrispettivo")
    protected String ivaCorrispettivo;
    @XmlElement(name = "IVAPrevendita")
    protected String ivaPrevendita;
    @XmlElement(name = "ImportoFigurativo")
    protected String importoFigurativo;
    @XmlElement(name = "IVAFigurativa")
    protected String ivaFigurativa;
    @XmlElement(name = "Partecipante")
    protected Partecipante partecipante;
    @XmlAttribute(name = "Annullamento")
    @XmlJavaTypeAdapter(CollapsedStringAdapter.class)
    protected String annullamento;

    /**
     * Recupera il valore della proprietà codiceAbbonamento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCodiceAbbonamento() {
        return codiceAbbonamento;
    }

    /**
     * Imposta il valore della proprietà codiceAbbonamento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCodiceAbbonamento(String value) {
        this.codiceAbbonamento = value;
    }

    /**
     * Recupera il valore della proprietà progressivoAbbonamento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getProgressivoAbbonamento() {
        return progressivoAbbonamento;
    }

    /**
     * Imposta il valore della proprietà progressivoAbbonamento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setProgressivoAbbonamento(String value) {
        this.progressivoAbbonamento = value;
    }

    /**
     * Recupera il valore della proprietà turno.
     * 
     * @return
     *     possible object is
     *     {@link Turno }
     *     
     */
    public Turno getTurno() {
        return turno;
    }

    /**
     * Imposta il valore della proprietà turno.
     * 
     * @param value
     *     allowed object is
     *     {@link Turno }
     *     
     */
    public void setTurno(Turno value) {
        this.turno = value;
    }

    /**
     * Recupera il valore della proprietà quantitaEventiAbilitati.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getQuantitaEventiAbilitati() {
        return quantitaEventiAbilitati;
    }

    /**
     * Imposta il valore della proprietà quantitaEventiAbilitati.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setQuantitaEventiAbilitati(String value) {
        this.quantitaEventiAbilitati = value;
    }

    /**
     * Recupera il valore della proprietà validita.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getValidita() {
        return validita;
    }

    /**
     * Imposta il valore della proprietà validita.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setValidita(String value) {
        this.validita = value;
    }

    /**
     * Recupera il valore della proprietà rateo.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getRateo() {
        return rateo;
    }

    /**
     * Imposta il valore della proprietà rateo.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setRateo(String value) {
        this.rateo = value;
    }

    /**
     * Recupera il valore della proprietà rateoIntrattenimenti.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getRateoIntrattenimenti() {
        return rateoIntrattenimenti;
    }

    /**
     * Imposta il valore della proprietà rateoIntrattenimenti.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setRateoIntrattenimenti(String value) {
        this.rateoIntrattenimenti = value;
    }

    /**
     * Recupera il valore della proprietà rateoIVA.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getRateoIVA() {
        return rateoIVA;
    }

    /**
     * Imposta il valore della proprietà rateoIVA.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setRateoIVA(String value) {
        this.rateoIVA = value;
    }

    /**
     * Recupera il valore della proprietà corrispettivoLordo.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCorrispettivoLordo() {
        return corrispettivoLordo;
    }

    /**
     * Imposta il valore della proprietà corrispettivoLordo.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCorrispettivoLordo(String value) {
        this.corrispettivoLordo = value;
    }

    /**
     * Recupera il valore della proprietà prevendita.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getPrevendita() {
        return prevendita;
    }

    /**
     * Imposta il valore della proprietà prevendita.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setPrevendita(String value) {
        this.prevendita = value;
    }

    /**
     * Recupera il valore della proprietà ivaCorrispettivo.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIVACorrispettivo() {
        return ivaCorrispettivo;
    }

    /**
     * Imposta il valore della proprietà ivaCorrispettivo.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIVACorrispettivo(String value) {
        this.ivaCorrispettivo = value;
    }

    /**
     * Recupera il valore della proprietà ivaPrevendita.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIVAPrevendita() {
        return ivaPrevendita;
    }

    /**
     * Imposta il valore della proprietà ivaPrevendita.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIVAPrevendita(String value) {
        this.ivaPrevendita = value;
    }

    /**
     * Recupera il valore della proprietà importoFigurativo.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getImportoFigurativo() {
        return importoFigurativo;
    }

    /**
     * Imposta il valore della proprietà importoFigurativo.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setImportoFigurativo(String value) {
        this.importoFigurativo = value;
    }

    /**
     * Recupera il valore della proprietà ivaFigurativa.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIVAFigurativa() {
        return ivaFigurativa;
    }

    /**
     * Imposta il valore della proprietà ivaFigurativa.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIVAFigurativa(String value) {
        this.ivaFigurativa = value;
    }

    /**
     * Recupera il valore della proprietà partecipante.
     * 
     * @return
     *     possible object is
     *     {@link Partecipante }
     *     
     */
    public Partecipante getPartecipante() {
        return partecipante;
    }

    /**
     * Imposta il valore della proprietà partecipante.
     * 
     * @param value
     *     allowed object is
     *     {@link Partecipante }
     *     
     */
    public void setPartecipante(Partecipante value) {
        this.partecipante = value;
    }

    /**
     * Recupera il valore della proprietà annullamento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getAnnullamento() {
        if (annullamento == null) {
            return "N";
        } else {
            return annullamento;
        }
    }

    /**
     * Imposta il valore della proprietà annullamento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setAnnullamento(String value) {
        this.annullamento = value;
    }

	@Override
	public String toString() {
		return (codiceAbbonamento != null ? "codiceAbbonamento: " + codiceAbbonamento + ",  " : "")
				+ (progressivoAbbonamento != null ? "progressivoAbbonamento: " + progressivoAbbonamento + ",  " : "")
				+ (turno != null ? "turno: " + turno + ",  " : "")
				+ (quantitaEventiAbilitati != null ? "quantitaEventiAbilitati: " + quantitaEventiAbilitati + ",  " : "")
				+ (rateo != null ? "rateo: " + rateo + ",  " : "")
				+ (corrispettivoLordo != null ? "corrispettivoLordo: " + corrispettivoLordo + ",  " : "")
				+ (annullamento != null ? "annullamento: " + annullamento : "");
	}

    
    
}
