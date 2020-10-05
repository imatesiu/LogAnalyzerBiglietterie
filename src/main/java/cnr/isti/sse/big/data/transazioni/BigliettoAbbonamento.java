//
// Questo file � stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andr� persa durante la ricompilazione dello schema di origine. 
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
     * Recupera il valore della propriet� codiceAbbonamento.
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
     * Imposta il valore della propriet� codiceAbbonamento.
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
     * Recupera il valore della propriet� progressivoAbbonamento.
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
     * Imposta il valore della propriet� progressivoAbbonamento.
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
     * Recupera il valore della propriet� codiceFiscale.
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
     * Imposta il valore della propriet� codiceFiscale.
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

}
