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
 *         &lt;element ref="{}CodiceLocale"/>
 *         &lt;element ref="{}DataEvento"/>
 *         &lt;element ref="{}OraEvento"/>
 *         &lt;element ref="{}TipoGenere"/>
 *         &lt;element ref="{}Titolo"/>
 *         &lt;element ref="{}CodiceAbbonamento"/>
 *         &lt;element ref="{}ProgressivoAbbonamento"/>
 *         &lt;element ref="{}CodiceFiscale"/>
 *         &lt;element ref="{}ImportoFigurativo"/>
 *         &lt;element ref="{}IVAFigurativa"/>
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
    "codiceLocale",
    "dataEvento",
    "oraEvento",
    "tipoGenere",
    "titolo",
    "codiceAbbonamento",
    "progressivoAbbonamento",
    "codiceFiscale",
    "importoFigurativo",
    "ivaFigurativa",
    "partecipante"
})
@XmlRootElement(name = "BigliettoAbbonamento")
public class BigliettoAbbonamento {

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
    @XmlElement(name = "CodiceAbbonamento", required = true)
    protected String codiceAbbonamento;
    @XmlElement(name = "ProgressivoAbbonamento", required = true)
    protected String progressivoAbbonamento;
    @XmlElement(name = "CodiceFiscale", required = true)
    protected String codiceFiscale;
    @XmlElement(name = "ImportoFigurativo", required = true)
    protected String importoFigurativo;
    @XmlElement(name = "IVAFigurativa", required = true)
    protected String ivaFigurativa;
    @XmlElement(name = "Partecipante")
    protected Partecipante partecipante;
    @XmlAttribute(name = "Annullamento")
    @XmlJavaTypeAdapter(CollapsedStringAdapter.class)
    protected String annullamento;

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
     * Recupera il valore della proprietà codiceFiscale.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCodiceFiscale() {
        return codiceFiscale;
    }

    /**
     * Imposta il valore della proprietà codiceFiscale.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCodiceFiscale(String value) {
        this.codiceFiscale = value;
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

}
