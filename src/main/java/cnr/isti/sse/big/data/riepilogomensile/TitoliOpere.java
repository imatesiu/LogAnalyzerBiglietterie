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
 *         &lt;element ref="{http://siae.it/mensile}Titolo"/>
 *         &lt;element ref="{http://siae.it/mensile}ProduttoreCinema" minOccurs="0"/>
 *         &lt;element ref="{http://siae.it/mensile}Autore" minOccurs="0"/>
 *         &lt;element ref="{http://siae.it/mensile}Esecutore" minOccurs="0"/>
 *         &lt;element ref="{http://siae.it/mensile}Nazionalita" minOccurs="0"/>
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
    "titolo",
    "produttoreCinema",
    "autore",
    "esecutore",
    "nazionalita"
})
@XmlRootElement(name = "TitoliOpere")
public class TitoliOpere {

    @XmlElement(name = "Titolo", required = true)
    protected String titolo;
    @XmlElement(name = "ProduttoreCinema")
    protected String produttoreCinema;
    @XmlElement(name = "Autore")
    protected String autore;
    @XmlElement(name = "Esecutore")
    protected String esecutore;
    @XmlElement(name = "Nazionalita")
    protected String nazionalita;

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
     * Recupera il valore della proprietà produttoreCinema.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getProduttoreCinema() {
        return produttoreCinema;
    }

    /**
     * Imposta il valore della proprietà produttoreCinema.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setProduttoreCinema(String value) {
        this.produttoreCinema = value;
    }

    /**
     * Recupera il valore della proprietà autore.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getAutore() {
        return autore;
    }

    /**
     * Imposta il valore della proprietà autore.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setAutore(String value) {
        this.autore = value;
    }

    /**
     * Recupera il valore della proprietà esecutore.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getEsecutore() {
        return esecutore;
    }

    /**
     * Imposta il valore della proprietà esecutore.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setEsecutore(String value) {
        this.esecutore = value;
    }

    /**
     * Recupera il valore della proprietà nazionalita.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getNazionalita() {
        return nazionalita;
    }

    /**
     * Imposta il valore della proprietà nazionalita.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setNazionalita(String value) {
        this.nazionalita = value;
    }

}
