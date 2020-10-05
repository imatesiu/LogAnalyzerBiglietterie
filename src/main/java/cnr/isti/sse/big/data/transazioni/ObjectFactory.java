//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.10.05 alle 12:50:22 PM CEST 
//


package cnr.isti.sse.big.data.transazioni;

import javax.xml.bind.JAXBElement;
import javax.xml.bind.annotation.XmlElementDecl;
import javax.xml.bind.annotation.XmlRegistry;
import javax.xml.namespace.QName;


/**
 * This object contains factory methods for each 
 * Java content interface and Java element interface 
 * generated in the cnr.isti.sse.big.data.transazioni package. 
 * <p>An ObjectFactory allows you to programatically 
 * construct new instances of the Java representation 
 * for XML content. The Java representation of XML 
 * content can consist of schema derived interfaces 
 * and classes representing the binding of schema 
 * type definitions, element declarations and model 
 * groups.  Factory methods for each of these are 
 * provided in this class.
 * 
 */
@XmlRegistry
public class ObjectFactory {

    private final static QName _CRO_QNAME = new QName("", "CRO");
    private final static QName _DataOraEsecuzionePagamento_QNAME = new QName("", "DataOraEsecuzionePagamento");
    private final static QName _IVACorrispettivo_QNAME = new QName("", "IVACorrispettivo");
    private final static QName _Titolo_QNAME = new QName("", "Titolo");
    private final static QName _EmailAcquirente_QNAME = new QName("", "EmailAcquirente");
    private final static QName _IndirizzoIPTransazione_QNAME = new QName("", "IndirizzoIPTransazione");
    private final static QName _CodiceFiscale_QNAME = new QName("", "CodiceFiscale");
    private final static QName _DataOraRegistrazione_QNAME = new QName("", "DataOraRegistrazione");
    private final static QName _CellulareAcquirente_QNAME = new QName("", "CellulareAcquirente");
    private final static QName _MetodoSpedizioneTitolo_QNAME = new QName("", "MetodoSpedizioneTitolo");
    private final static QName _TipoGenere_QNAME = new QName("", "TipoGenere");
    private final static QName _CodicePrestazione_QNAME = new QName("", "CodicePrestazione");
    private final static QName _Quantita_QNAME = new QName("", "Quantita");
    private final static QName _CorrispettivoLordo_QNAME = new QName("", "CorrispettivoLordo");
    private final static QName _Prevendita_QNAME = new QName("", "Prevendita");
    private final static QName _CodiceAbbonamento_QNAME = new QName("", "CodiceAbbonamento");
    private final static QName _CodiceUnivocoNumeroTransazione_QNAME = new QName("", "CodiceUnivocoNumeroTransazione");
    private final static QName _Validita_QNAME = new QName("", "Validita");
    private final static QName _IndirizzoSpedizioneTitolo_QNAME = new QName("", "IndirizzoSpedizioneTitolo");
    private final static QName _Nome_QNAME = new QName("", "Nome");
    private final static QName _OriginaleAnnullato_QNAME = new QName("", "OriginaleAnnullato");
    private final static QName _DataEvento_QNAME = new QName("", "DataEvento");
    private final static QName _Rateo_QNAME = new QName("", "Rateo");
    private final static QName _OriginaleRiferimentoAnnullamento_QNAME = new QName("", "OriginaleRiferimentoAnnullamento");
    private final static QName _TipoProvento_QNAME = new QName("", "TipoProvento");
    private final static QName _QuantitaEventiAbilitati_QNAME = new QName("", "QuantitaEventiAbilitati");
    private final static QName _CodiceLocale_QNAME = new QName("", "CodiceLocale");
    private final static QName _ProgressivoAbbonamento_QNAME = new QName("", "ProgressivoAbbonamento");
    private final static QName _IndirizzoIPRegistrazione_QNAME = new QName("", "IndirizzoIPRegistrazione");
    private final static QName _CodiceUnivocoAcquirente_QNAME = new QName("", "CodiceUnivocoAcquirente");
    private final static QName _CartaRiferimentoAnnullamento_QNAME = new QName("", "CartaRiferimentoAnnullamento");
    private final static QName _DataOraInizioCheckout_QNAME = new QName("", "DataOraInizioCheckout");
    private final static QName _ImportoPrestazione_QNAME = new QName("", "ImportoPrestazione");
    private final static QName _RateoIntrattenimenti_QNAME = new QName("", "RateoIntrattenimenti");
    private final static QName _RateoIVA_QNAME = new QName("", "RateoIVA");
    private final static QName _CausaleRiferimentoAnnullamento_QNAME = new QName("", "CausaleRiferimentoAnnullamento");
    private final static QName _IVAPrevendita_QNAME = new QName("", "IVAPrevendita");
    private final static QName _ImportoFigurativo_QNAME = new QName("", "ImportoFigurativo");
    private final static QName _IVAFigurativa_QNAME = new QName("", "IVAFigurativa");
    private final static QName _OraEvento_QNAME = new QName("", "OraEvento");
    private final static QName _Cognome_QNAME = new QName("", "Cognome");

    /**
     * Create a new ObjectFactory that can be used to create new instances of schema derived classes for package: cnr.isti.sse.big.data.transazioni
     * 
     */
    public ObjectFactory() {
    }

    /**
     * Create an instance of {@link LogTransazione }
     * 
     */
    public LogTransazione createLogTransazione() {
        return new LogTransazione();
    }

    /**
     * Create an instance of {@link Transazione }
     * 
     */
    public Transazione createTransazione() {
        return new Transazione();
    }

    /**
     * Create an instance of {@link TitoloAccesso }
     * 
     */
    public TitoloAccesso createTitoloAccesso() {
        return new TitoloAccesso();
    }

    /**
     * Create an instance of {@link Complementare }
     * 
     */
    public Complementare createComplementare() {
        return new Complementare();
    }

    /**
     * Create an instance of {@link Partecipante }
     * 
     */
    public Partecipante createPartecipante() {
        return new Partecipante();
    }

    /**
     * Create an instance of {@link Abbonamento }
     * 
     */
    public Abbonamento createAbbonamento() {
        return new Abbonamento();
    }

    /**
     * Create an instance of {@link Turno }
     * 
     */
    public Turno createTurno() {
        return new Turno();
    }

    /**
     * Create an instance of {@link BigliettoAbbonamento }
     * 
     */
    public BigliettoAbbonamento createBigliettoAbbonamento() {
        return new BigliettoAbbonamento();
    }

    /**
     * Create an instance of {@link AcquirenteRegistrazione }
     * 
     */
    public AcquirenteRegistrazione createAcquirenteRegistrazione() {
        return new AcquirenteRegistrazione();
    }

    /**
     * Create an instance of {@link AcquirenteTransazione }
     * 
     */
    public AcquirenteTransazione createAcquirenteTransazione() {
        return new AcquirenteTransazione();
    }

    /**
     * Create an instance of {@link RiferimentoAnnullamento }
     * 
     */
    public RiferimentoAnnullamento createRiferimentoAnnullamento() {
        return new RiferimentoAnnullamento();
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "CRO")
    public JAXBElement<String> createCRO(String value) {
        return new JAXBElement<String>(_CRO_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "DataOraEsecuzionePagamento")
    public JAXBElement<String> createDataOraEsecuzionePagamento(String value) {
        return new JAXBElement<String>(_DataOraEsecuzionePagamento_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "IVACorrispettivo")
    public JAXBElement<String> createIVACorrispettivo(String value) {
        return new JAXBElement<String>(_IVACorrispettivo_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "Titolo")
    public JAXBElement<String> createTitolo(String value) {
        return new JAXBElement<String>(_Titolo_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "EmailAcquirente")
    public JAXBElement<String> createEmailAcquirente(String value) {
        return new JAXBElement<String>(_EmailAcquirente_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "IndirizzoIPTransazione")
    public JAXBElement<String> createIndirizzoIPTransazione(String value) {
        return new JAXBElement<String>(_IndirizzoIPTransazione_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "CodiceFiscale")
    public JAXBElement<String> createCodiceFiscale(String value) {
        return new JAXBElement<String>(_CodiceFiscale_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "DataOraRegistrazione")
    public JAXBElement<String> createDataOraRegistrazione(String value) {
        return new JAXBElement<String>(_DataOraRegistrazione_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "CellulareAcquirente")
    public JAXBElement<String> createCellulareAcquirente(String value) {
        return new JAXBElement<String>(_CellulareAcquirente_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "MetodoSpedizioneTitolo")
    public JAXBElement<String> createMetodoSpedizioneTitolo(String value) {
        return new JAXBElement<String>(_MetodoSpedizioneTitolo_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "TipoGenere")
    public JAXBElement<String> createTipoGenere(String value) {
        return new JAXBElement<String>(_TipoGenere_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "CodicePrestazione")
    public JAXBElement<String> createCodicePrestazione(String value) {
        return new JAXBElement<String>(_CodicePrestazione_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "Quantita")
    public JAXBElement<String> createQuantita(String value) {
        return new JAXBElement<String>(_Quantita_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "CorrispettivoLordo")
    public JAXBElement<String> createCorrispettivoLordo(String value) {
        return new JAXBElement<String>(_CorrispettivoLordo_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "Prevendita")
    public JAXBElement<String> createPrevendita(String value) {
        return new JAXBElement<String>(_Prevendita_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "CodiceAbbonamento")
    public JAXBElement<String> createCodiceAbbonamento(String value) {
        return new JAXBElement<String>(_CodiceAbbonamento_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "CodiceUnivocoNumeroTransazione")
    public JAXBElement<String> createCodiceUnivocoNumeroTransazione(String value) {
        return new JAXBElement<String>(_CodiceUnivocoNumeroTransazione_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "Validita")
    public JAXBElement<String> createValidita(String value) {
        return new JAXBElement<String>(_Validita_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "IndirizzoSpedizioneTitolo")
    public JAXBElement<String> createIndirizzoSpedizioneTitolo(String value) {
        return new JAXBElement<String>(_IndirizzoSpedizioneTitolo_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "Nome")
    public JAXBElement<String> createNome(String value) {
        return new JAXBElement<String>(_Nome_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "OriginaleAnnullato")
    public JAXBElement<String> createOriginaleAnnullato(String value) {
        return new JAXBElement<String>(_OriginaleAnnullato_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "DataEvento")
    public JAXBElement<String> createDataEvento(String value) {
        return new JAXBElement<String>(_DataEvento_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "Rateo")
    public JAXBElement<String> createRateo(String value) {
        return new JAXBElement<String>(_Rateo_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "OriginaleRiferimentoAnnullamento")
    public JAXBElement<String> createOriginaleRiferimentoAnnullamento(String value) {
        return new JAXBElement<String>(_OriginaleRiferimentoAnnullamento_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "TipoProvento")
    public JAXBElement<String> createTipoProvento(String value) {
        return new JAXBElement<String>(_TipoProvento_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "QuantitaEventiAbilitati")
    public JAXBElement<String> createQuantitaEventiAbilitati(String value) {
        return new JAXBElement<String>(_QuantitaEventiAbilitati_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "CodiceLocale")
    public JAXBElement<String> createCodiceLocale(String value) {
        return new JAXBElement<String>(_CodiceLocale_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "ProgressivoAbbonamento")
    public JAXBElement<String> createProgressivoAbbonamento(String value) {
        return new JAXBElement<String>(_ProgressivoAbbonamento_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "IndirizzoIPRegistrazione")
    public JAXBElement<String> createIndirizzoIPRegistrazione(String value) {
        return new JAXBElement<String>(_IndirizzoIPRegistrazione_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "CodiceUnivocoAcquirente")
    public JAXBElement<String> createCodiceUnivocoAcquirente(String value) {
        return new JAXBElement<String>(_CodiceUnivocoAcquirente_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "CartaRiferimentoAnnullamento")
    public JAXBElement<String> createCartaRiferimentoAnnullamento(String value) {
        return new JAXBElement<String>(_CartaRiferimentoAnnullamento_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "DataOraInizioCheckout")
    public JAXBElement<String> createDataOraInizioCheckout(String value) {
        return new JAXBElement<String>(_DataOraInizioCheckout_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "ImportoPrestazione")
    public JAXBElement<String> createImportoPrestazione(String value) {
        return new JAXBElement<String>(_ImportoPrestazione_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "RateoIntrattenimenti")
    public JAXBElement<String> createRateoIntrattenimenti(String value) {
        return new JAXBElement<String>(_RateoIntrattenimenti_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "RateoIVA")
    public JAXBElement<String> createRateoIVA(String value) {
        return new JAXBElement<String>(_RateoIVA_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "CausaleRiferimentoAnnullamento")
    public JAXBElement<String> createCausaleRiferimentoAnnullamento(String value) {
        return new JAXBElement<String>(_CausaleRiferimentoAnnullamento_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "IVAPrevendita")
    public JAXBElement<String> createIVAPrevendita(String value) {
        return new JAXBElement<String>(_IVAPrevendita_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "ImportoFigurativo")
    public JAXBElement<String> createImportoFigurativo(String value) {
        return new JAXBElement<String>(_ImportoFigurativo_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "IVAFigurativa")
    public JAXBElement<String> createIVAFigurativa(String value) {
        return new JAXBElement<String>(_IVAFigurativa_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "OraEvento")
    public JAXBElement<String> createOraEvento(String value) {
        return new JAXBElement<String>(_OraEvento_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "", name = "Cognome")
    public JAXBElement<String> createCognome(String value) {
        return new JAXBElement<String>(_Cognome_QNAME, String.class, null, value);
    }

}
