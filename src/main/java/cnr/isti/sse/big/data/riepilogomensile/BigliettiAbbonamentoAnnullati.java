//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.11.17 alle 02:47:25 PM CET 
//


package cnr.isti.sse.big.data.riepilogomensile;

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
 *         &lt;element ref="{http://siae.it/mensile}CodiceFiscale" minOccurs="0"/>
 *         &lt;element ref="{http://siae.it/mensile}CodiceAbbonamento"/>
 *         &lt;element ref="{http://siae.it/mensile}TipoTitolo"/>
 *         &lt;element ref="{http://siae.it/mensile}Quantita"/>
 *         &lt;element ref="{http://siae.it/mensile}ImportoFigurativo"/>
 *         &lt;element ref="{http://siae.it/mensile}IVAFigurativa"/>
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
    "codiceFiscale",
    "codiceAbbonamento",
    "tipoTitolo",
    "quantita",
    "importoFigurativo",
    "ivaFigurativa"
})
@XmlRootElement(name = "BigliettiAbbonamentoAnnullati")
public class BigliettiAbbonamentoAnnullati {

    @XmlElement(name = "CodiceFiscale")
    protected String codiceFiscale;
    @XmlElement(name = "CodiceAbbonamento", required = true)
    protected String codiceAbbonamento;
    @XmlElement(name = "TipoTitolo", required = true)
    protected String tipoTitolo;
    @XmlElement(name = "Quantita", required = true)
    protected String quantita;
    @XmlElement(name = "ImportoFigurativo", required = true)
    protected String importoFigurativo;
    @XmlElement(name = "IVAFigurativa", required = true)
    protected String ivaFigurativa;

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
     * Recupera il valore della proprietà tipoTitolo.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTipoTitolo() {
        return tipoTitolo;
    }

    /**
     * Imposta il valore della proprietà tipoTitolo.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTipoTitolo(String value) {
        this.tipoTitolo = value;
    }

    /**
     * Recupera il valore della proprietà quantita.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getQuantita() {
        return quantita;
    }

    /**
     * Imposta il valore della proprietà quantita.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setQuantita(String value) {
        this.quantita = value;
    }

    /**
     * Recupera il valore della proprietà ImportoFigurativo.
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
     * Imposta il valore della proprietà ImportoFigurativo.
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
     * Recupera il valore della proprietà IVAFigurativa.
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
     * Imposta il valore della proprietà IVAFigurativa.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIVAFigurativa(String value) {
        this.ivaFigurativa = value;
    }

}
