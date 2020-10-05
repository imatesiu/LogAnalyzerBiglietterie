//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.10.05 alle 12:50:22 PM CEST 
//


package cnr.isti.sse.big.data.transazioni;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;


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
 *         &lt;element ref="{}CodiceUnivocoNumeroTransazione"/>
 *         &lt;element ref="{}CellulareAcquirente" minOccurs="0"/>
 *         &lt;element ref="{}EmailAcquirente" minOccurs="0"/>
 *         &lt;element ref="{}IndirizzoIPTransazione" minOccurs="0"/>
 *         &lt;element ref="{}DataOraInizioCheckout"/>
 *         &lt;element ref="{}DataOraEsecuzionePagamento"/>
 *         &lt;element ref="{}CRO" minOccurs="0"/>
 *         &lt;element ref="{}MetodoSpedizioneTitolo"/>
 *         &lt;element ref="{}IndirizzoSpedizioneTitolo" minOccurs="0"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "codiceUnivocoNumeroTransazione",
    "cellulareAcquirente",
    "emailAcquirente",
    "indirizzoIPTransazione",
    "dataOraInizioCheckout",
    "dataOraEsecuzionePagamento",
    "cro",
    "metodoSpedizioneTitolo",
    "indirizzoSpedizioneTitolo"
})
@XmlRootElement(name = "AcquirenteTransazione")
public class AcquirenteTransazione {

    @XmlElement(name = "CodiceUnivocoNumeroTransazione", required = true)
    protected String codiceUnivocoNumeroTransazione;
    @XmlElement(name = "CellulareAcquirente")
    protected String cellulareAcquirente;
    @XmlElement(name = "EmailAcquirente")
    protected String emailAcquirente;
    @XmlElement(name = "IndirizzoIPTransazione")
    protected String indirizzoIPTransazione;
    @XmlElement(name = "DataOraInizioCheckout", required = true)
    protected String dataOraInizioCheckout;
    @XmlElement(name = "DataOraEsecuzionePagamento", required = true)
    protected String dataOraEsecuzionePagamento;
    @XmlElement(name = "CRO")
    protected String cro;
    @XmlElement(name = "MetodoSpedizioneTitolo", required = true)
    protected String metodoSpedizioneTitolo;
    @XmlElement(name = "IndirizzoSpedizioneTitolo")
    protected String indirizzoSpedizioneTitolo;

    /**
     * Recupera il valore della proprietà codiceUnivocoNumeroTransazione.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCodiceUnivocoNumeroTransazione() {
        return codiceUnivocoNumeroTransazione;
    }

    /**
     * Imposta il valore della proprietà codiceUnivocoNumeroTransazione.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCodiceUnivocoNumeroTransazione(String value) {
        this.codiceUnivocoNumeroTransazione = value;
    }

    /**
     * Recupera il valore della proprietà cellulareAcquirente.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCellulareAcquirente() {
        return cellulareAcquirente;
    }

    /**
     * Imposta il valore della proprietà cellulareAcquirente.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCellulareAcquirente(String value) {
        this.cellulareAcquirente = value;
    }

    /**
     * Recupera il valore della proprietà emailAcquirente.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getEmailAcquirente() {
        return emailAcquirente;
    }

    /**
     * Imposta il valore della proprietà emailAcquirente.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setEmailAcquirente(String value) {
        this.emailAcquirente = value;
    }

    /**
     * Recupera il valore della proprietà indirizzoIPTransazione.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIndirizzoIPTransazione() {
        return indirizzoIPTransazione;
    }

    /**
     * Imposta il valore della proprietà indirizzoIPTransazione.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIndirizzoIPTransazione(String value) {
        this.indirizzoIPTransazione = value;
    }

    /**
     * Recupera il valore della proprietà dataOraInizioCheckout.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDataOraInizioCheckout() {
        return dataOraInizioCheckout;
    }

    /**
     * Imposta il valore della proprietà dataOraInizioCheckout.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDataOraInizioCheckout(String value) {
        this.dataOraInizioCheckout = value;
    }

    /**
     * Recupera il valore della proprietà dataOraEsecuzionePagamento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDataOraEsecuzionePagamento() {
        return dataOraEsecuzionePagamento;
    }

    /**
     * Imposta il valore della proprietà dataOraEsecuzionePagamento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDataOraEsecuzionePagamento(String value) {
        this.dataOraEsecuzionePagamento = value;
    }

    /**
     * Recupera il valore della proprietà cro.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCRO() {
        return cro;
    }

    /**
     * Imposta il valore della proprietà cro.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCRO(String value) {
        this.cro = value;
    }

    /**
     * Recupera il valore della proprietà metodoSpedizioneTitolo.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getMetodoSpedizioneTitolo() {
        return metodoSpedizioneTitolo;
    }

    /**
     * Imposta il valore della proprietà metodoSpedizioneTitolo.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setMetodoSpedizioneTitolo(String value) {
        this.metodoSpedizioneTitolo = value;
    }

    /**
     * Recupera il valore della proprietà indirizzoSpedizioneTitolo.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIndirizzoSpedizioneTitolo() {
        return indirizzoSpedizioneTitolo;
    }

    /**
     * Imposta il valore della proprietà indirizzoSpedizioneTitolo.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIndirizzoSpedizioneTitolo(String value) {
        this.indirizzoSpedizioneTitolo = value;
    }

}
