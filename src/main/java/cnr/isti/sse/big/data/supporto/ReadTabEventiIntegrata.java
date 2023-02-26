package cnr.isti.sse.big.data.supporto;

import cnr.isti.sse.big.rest.impl.ApiRestRPGBig;

import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Unmarshaller;
import java.io.InputStream;
import java.util.List;

import static org.junit.Assert.assertNotNull;

public class ReadTabEventiIntegrata {

    private static  org.apache.logging.log4j.Logger log = org.apache.logging.log4j.LogManager.getLogger(ReadTabEventiIntegrata.class);

    private static TabEventiIntegrata TTabEventiIntegrata;

    public static TabEventiIntegrata readTabEventiIntegrata(){
        if(TTabEventiIntegrata==null){
            return readTabEventi();
        }
        return  TTabEventiIntegrata;
    }

    public static TabEvento getTabEvento(String evento){
        TTabEventiIntegrata = readTabEventiIntegrata();
        List<TabEvento> list = TTabEventiIntegrata.getEvento();
        for (TabEvento tabe: list) {
            if(tabe.getCodice().equals(evento))
                return tabe;
        }

        return null;
    }

    private static TabEventiIntegrata readTabEventi(){
        InputStream is = ReadTabEventiIntegrata.class.getClassLoader().getResourceAsStream("TabEventi.xml");
        assertNotNull(is);

        JAXBContext jaxbContext;
        try {
            jaxbContext = JAXBContext.newInstance(TabEventiIntegrata.class);

            Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
            //StringReader reader = new StringReader(EsitoOperazione);

             TTabEventiIntegrata = (TabEventiIntegrata) unmarshaller.unmarshal(is);

            return TTabEventiIntegrata;
        } catch (JAXBException e) {
            log.error(e.getLocalizedMessage());
        }
        return null;
    }

}
