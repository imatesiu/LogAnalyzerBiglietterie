package cnr.isti.sse.big.rest.impl;
import java.io.IOException;
import java.io.InputStream;
import java.io.StringReader;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.QueryParam;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.Response.Status;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Unmarshaller;
import javax.xml.bind.annotation.XmlElement;

import org.apache.commons.io.IOUtils;
import org.apache.commons.lang3.tuple.ImmutableTriple;
import org.glassfish.grizzly.utils.Pair;
import org.glassfish.jersey.media.multipart.FormDataContentDisposition;
import org.glassfish.jersey.media.multipart.FormDataParam;

import cnr.isti.sse.big.data.riepilogomensile.Abbonamenti;
import cnr.isti.sse.big.data.riepilogomensile.AbbonamentiFissi;
import cnr.isti.sse.big.data.riepilogomensile.AltriProventiGenerici;
import cnr.isti.sse.big.data.riepilogomensile.BigliettiAbbonamento;
import cnr.isti.sse.big.data.riepilogomensile.BigliettiAbbonamentoAnnullati;
import cnr.isti.sse.big.data.riepilogomensile.Evento;
import cnr.isti.sse.big.data.riepilogomensile.OrdineDiPosto;
import cnr.isti.sse.big.data.riepilogomensile.Organizzatore;
import cnr.isti.sse.big.data.riepilogomensile.RiepilogoMensile;
import cnr.isti.sse.big.data.riepilogomensile.TitoliAccesso;
import cnr.isti.sse.big.data.riepilogomensile.TitoliAccessoIVAPreassolta;
import cnr.isti.sse.big.data.riepilogomensile.TitoliAnnullati;
import cnr.isti.sse.big.data.riepilogomensile.TitoliIVAPreassoltaAnnullati;
import cnr.isti.sse.big.util.Utility;
import io.swagger.v3.oas.annotations.Hidden;
import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.parameters.RequestBody;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.servers.Server;



@OpenAPIDefinition(info = @Info(title = "APID Service", version = "0.1"), servers = {@Server(url="/v1/dispositivi")
})
@Consumes(MediaType.MULTIPART_FORM_DATA)
// @Produces(MediaType.APPLICATION_XML)
@Path("/biglietterie")
public class ApiRestRPMBig {
	
	private static  org.apache.logging.log4j.Logger log = org.apache.logging.log4j.LogManager.getLogger(ApiRestRPMBig.class);

	@Path("/RPM")
	@POST
	@ApiResponse(
	        responseCode = "200",
	        content = @Content(
	            mediaType = MediaType.APPLICATION_XML,
	            		schema = @Schema(implementation = String.class)
	        ),
	        description = "."
	    )
	@RequestBody(content = @Content(
			mediaType = MediaType.MULTIPART_FORM_DATA,
			schema = @Schema(implementation = RiepilogoMensile.class)
			),
	description = "." )
	public String putRPM(byte[] rpg, @Context HttpServletRequest request, @Context HttpServletResponse response)
			throws JAXBException {// DatiCorrispettiviType Corrispettivi,
		// @Context HttpServletRequest request){
		response.setHeader("Connection", "Close");
		log.info("****************RPM********************");
		try{
			
			log.info("Message from: "+request.getRemoteAddr());
			
			 boolean	result = Utility.verifyPKCS7(rpg);
				log.info(result);
				
				byte[] t = 	Utility.getData(rpg);
				String rmensile = new String(t);
				String mensile = rmensile.replaceAll("<!DOCTYPE RiepilogoMensile SYSTEM.*d\">", "");
			
			JAXBContext jaxbContext = JAXBContext.newInstance(RiepilogoMensile.class);
			Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
			Utility.validateXmlRiepilogoMensile(unmarshaller);	
			
			StringReader reader = new StringReader(mensile);
			RiepilogoMensile RPM = (RiepilogoMensile) unmarshaller.unmarshal(reader);

			
			List<Organizzatore> organizzatori = RPM.getOrganizzatore();
			
			
			Utility.check(organizzatori);
			
			String text = "KO";
			return text;
			//throw new WebApplicationException(Response.status(406).entity(text).build());
		
		
		
		} catch (Exception e) {
			e.printStackTrace();
			log.error(e);
		}
		return "";
		
	}
	
	@Path("/FileRPM")
	@POST
	@ApiResponse(
	        responseCode = "200",
	        content = @Content(
	            mediaType = MediaType.APPLICATION_XML,
	            		schema = @Schema(implementation = String.class)
	        ),
	        description = "."
	    )
	@RequestBody(content = @Content(
			mediaType = MediaType.MULTIPART_FORM_DATA,
			schema = @Schema(implementation = RiepilogoMensile.class)
			),
	description = "." )
	public String putRPM( @FormDataParam("file") InputStream uploadedInputStream,
			@FormDataParam("file") FormDataContentDisposition fileDetail, @Context HttpServletRequest request, @Context HttpServletResponse response)
			throws JAXBException {// DatiCorrispettiviType Corrispettivi,
		// @Context HttpServletRequest request){
		response.setHeader("Connection", "Close");
		log.info("****************RPM********************");
		try{
			
			log.info("Message from: "+request.getRemoteAddr());
			byte[] rpg = IOUtils.toByteArray(uploadedInputStream);
			 boolean	result = Utility.verifyPKCS7(rpg);
				log.info(result);
				
				byte[] t = 	Utility.getData(rpg);
				String rmensile = new String(t);
				String mensile = rmensile.replaceAll("<!DOCTYPE RiepilogoMensile SYSTEM.*d\">", "");
			
			JAXBContext jaxbContext = JAXBContext.newInstance(RiepilogoMensile.class);
			Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
			Utility.validateXmlLogTransazione(unmarshaller);	
			
			StringReader reader = new StringReader(mensile);
			RiepilogoMensile RPM = (RiepilogoMensile) unmarshaller.unmarshal(reader);

			
			List<Organizzatore> organizzatori = RPM.getOrganizzatore();
			
			
			Utility.check(organizzatori);
			
			String text = "KO";
			return text;
			//throw new WebApplicationException(Response.status(406).entity(text).build());
		
		
		
		} catch (Exception e) {
			e.printStackTrace();
			log.error(e);
		}
		return "";
		
	}
	
	

}
