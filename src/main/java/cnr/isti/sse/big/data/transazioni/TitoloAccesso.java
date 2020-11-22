//
// Questo file � stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andr� persa durante la ricompilazione dello schema di origine. 
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
     * Recupera il valore della propriet� corrispettivoLordo.
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
     * Imposta il valore della propriet� corrispettivoLordo.
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
     * Recupera il valore della propriet� prevendita.
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
     * Imposta il valore della propriet� prevendita.
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
     * Recupera il valore della propriet� ivaCorrispettivo.
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
     * Imposta il valore della propriet� ivaCorrispettivo.
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
     * Recupera il valore della propriet� ivaPrevendita.
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
     * Imposta il valore della propriet� ivaPrevendita.
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
     * Recupera il valore della propriet� importoFigurativo.
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
     * Imposta il valore della propriet� importoFigurativo.
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
     * Recupera il valore della propriet� ivaFigurativa.
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
     * Imposta il valore della propriet� ivaFigurativa.
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
     * Recupera il valore della propriet� codiceLocale.
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
     * Imposta il valore della propriet� codiceLocale.
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
     * Recupera il valore della propriet� dataEvento.
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
     * Imposta il valore della propriet� dataEvento.
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
     * Recupera il valore della propriet� oraEvento.
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
     * Imposta il valore della propriet� oraEvento.
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
     * Recupera il valore della propriet� tipoGenere.
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
     * Imposta il valore della propriet� tipoGenere.
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
     * Recupera il valore della propriet� titolo.
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
     * Imposta il valore della propriet� titolo.
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
     * Recupera il valore della propriet� partecipante.
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
     * Imposta il valore della propriet� partecipante.
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
     * Recupera il valore della propriet� annullamento.
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
     * Imposta il valore della propriet� annullamento.
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
