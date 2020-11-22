//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.10.05 alle 12:50:22 PM CEST 
//


package cnr.isti.sse.big.data.transazioni;

import java.util.ArrayList;
import java.util.List;
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
 *         &lt;element ref="{}CorrispettivoLordo" minOccurs="0"/>
 *         &lt;element ref="{}Prevendita" minOccurs="0"/>
 *         &lt;element ref="{}IVACorrispettivo" minOccurs="0"/>
 *         &lt;element ref="{}IVAPrevendita" minOccurs="0"/>
 *         &lt;element ref="{}ImportoFigurativo" minOccurs="0"/>
 *         &lt;element ref="{}IVAFigurativa" minOccurs="0"/>
 *         &lt;element ref="{}CodiceLocale"/>
 *         &lt;element ref="{}DataEvento"/>
 *         &lt;element ref="{}OraEvento"/>
 *         &lt;element ref="{}TipoGenere"/>
 *         &lt;element ref="{}Titolo"/>
 *         &lt;element ref="{}Complementare" maxOccurs="unbounded" minOccurs="0"/>
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
    "corrispettivoLordo",
    "prevendita",
    "ivaCorrispettivo",
    "ivaPrevendita",
    "importoFigurativo",
    "ivaFigurativa",
    "codiceLocale",
    "dataEvento",
    "oraEvento",
    "tipoGenere",
    "titolo",
    "complementare",
    "partecipante"
})
@XmlRootElement(name = "TitoloAccesso")
public class TitoloAccesso {

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
    @XmlElement(name = "CodiceLocale", required = true)
    protected String codiceLocale;
    @XmlElement(name = "DataEvento", required = true)
    protected String dataEvento;
    @XmlElement(name = "OraEvento", required = true)
    protected String oraEvento;
    @XmlElement(name = "TipoGenere", required = true)
    protected String tipoGenere;
    @XmlElement(name = "Titolo", required = true)
    protected String titolo;
    @XmlElement(name = "Complementare")
    protected List<Complementare> complementare;
    @XmlElement(name = "Partecipante")
    protected Partecipante partecipante;
    @XmlAttribute(name = "Annullamento")
    @XmlJavaTypeAdapter(CollapsedStringAdapter.class)
    protected String annullamento;

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
     * Recupera il valore della proprietà codiceLocale.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCodiceLocale() {
        return codiceLocale;
    }

    /**
     * Imposta il valore della proprietà codiceLocale.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCodiceLocale(String value) {
        this.codiceLocale = value;
    }

    /**
     * Recupera il valore della proprietà dataEvento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDataEvento() {
        return dataEvento;
    }

    /**
     * Imposta il valore della proprietà dataEvento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDataEvento(String value) {
        this.dataEvento = value;
    }

    /**
     * Recupera il valore della proprietà oraEvento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getOraEvento() {
        return oraEvento;
    }

    /**
     * Imposta il valore della proprietà oraEvento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setOraEvento(String value) {
        this.oraEvento = value;
    }

    /**
     * Recupera il valore della proprietà tipoGenere.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTipoGenere() {
        return tipoGenere;
    }

    /**
     * Imposta il valore della proprietà tipoGenere.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTipoGenere(String value) {
        this.tipoGenere = value;
    }

    /**
     * Recupera il valore della proprietà titolo.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTitolo() {
        return titolo;
    }

    /**
     * Imposta il valore della proprietà titolo.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTitolo(String value) {
        this.titolo = value;
    }

    /**
     * Gets the value of the complementare property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the complementare property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getComplementare().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link Complementare }
     * 
     * 
     */
    public List<Complementare> getComplementare() {
        if (complementare == null) {
            complementare = new ArrayList<Complementare>();
        }
        return this.complementare;
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
		return (corrispettivoLordo != null ? "corrispettivoLordo: " + corrispettivoLordo + ",  " : "")
				+ (prevendita != null ? "prevendita: " + prevendita + ",  " : "")
				+ (titolo != null ? "titolo: " + titolo + ",  " : "")
				+ (annullamento != null ? "annullamento: " + annullamento : "");
	}
    
    

}
