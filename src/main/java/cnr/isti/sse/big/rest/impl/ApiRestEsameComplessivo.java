package cnr.isti.sse.big.rest.impl;

import java.io.InputStream;
import java.io.StringReader;
import java.util.List;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.ws.rs.Consumes;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Unmarshaller;

import org.apache.commons.io.IOUtils;
import org.glassfish.jersey.media.multipart.FormDataBodyPart;
import org.glassfish.jersey.media.multipart.FormDataContentDisposition;
import org.glassfish.jersey.media.multipart.FormDataParam;

import cnr.isti.sse.big.data.reply.accessi.RiepilogoControlloAccessi;
import cnr.isti.sse.big.data.reply.accessi.lta.LTAGiornaliera;
import cnr.isti.sse.big.data.riepilogogiornaliero.RiepilogoGiornaliero;
import cnr.isti.sse.big.data.riepilogomensile.RiepilogoMensile;
import cnr.isti.sse.big.data.sigillo.LogSigillo;
import cnr.isti.sse.big.data.transazioni.LogTransazione;
import cnr.isti.sse.big.rest.util.EsameComplessivo;
import cnr.isti.sse.big.util.Utility;
import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.parameters.RequestBody;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.servers.Server;

@OpenAPIDefinition(info = @Info(title = "APID Service", version = "0.1"), servers = {
		@Server(url = "/v1/dispositivi") })
//@Consumes(MediaType.MULTIPART_FORM_DATA)
// @Produces(MediaType.APPLICATION_XML)
@Path("/biglietterie")
public class ApiRestEsameComplessivo {

	private static org.apache.logging.log4j.Logger log = org.apache.logging.log4j.LogManager
			.getLogger(ApiRestEsameComplessivo.class);

	@Path("/EsameComplessivo")
	@POST
	@ApiResponse(responseCode = "200", content = @Content(mediaType = MediaType.APPLICATION_XML, schema = @Schema(implementation = String.class)), description = ".")
	@RequestBody(content = @Content(mediaType = MediaType.MULTIPART_FORM_DATA// ,
	// schema = @Schema(implementation = List<byte[]>.class)
	), description = ".")
	@Consumes(MediaType.MULTIPART_FORM_DATA)
	// @Produces(MediaType.APPLICATION_JSON)
	public String putFiles(@FormDataParam("files") List<FormDataBodyPart> uploadedInputStream,
			@FormDataParam("files") List<FormDataContentDisposition> fileDetail, @Context HttpServletRequest request,
			@Context HttpServletResponse response) throws JAXBException {// DatiCorrispettiviType Corrispettivi,
		// @Context HttpServletRequest request){
		response.setHeader("Connection", "Close");
		log.info("****************ESAME COMPLESSIVO********************");
		try {

			log.info("Message from: " + request.getRemoteAddr());

			EsameComplessivo e = new EsameComplessivo();
			byte[] t = new byte[1];
			int i = 0;
			for (FormDataBodyPart filePart : uploadedInputStream) {
				byte[] your_primitive_bytes = IOUtils.toByteArray(filePart.getEntityAs(InputStream.class));
				String NameFile = fileDetail.get(i).getFileName();
				log.info(NameFile);
				if (NameFile.contains("p7m") || NameFile.contains("P7M")) {
					try {
						boolean resul = Utility.verifyPKCS7(your_primitive_bytes);
						log.info(resul);
					} catch (Exception e1) {
						log.error(NameFile);
						log.error(e1.getLocalizedMessage());
					}
					t = Utility.getData(your_primitive_bytes);
				} else {
					t = your_primitive_bytes;
				}

				String Transazione = new String(t);
				Utility.checkDocType(Transazione);
				String LT = Transazione.replaceAll("<!DOCTYPE[^<>]*(?:<![^<>]*>[^<>]*)*d\">", "")
						.replaceAll("[^\\x20-\\x7e]", "");//
				LT = LT.replaceAll("<!DOCTYPE[^<>]*(?:<![^<>]*>[^<>]*)*d'>", "").replaceAll("[^\\x20-\\x7e]", "");//
				LT = LT.replaceAll("<!DOCTYPE[^<>]*(?:<![^<>]*>[^<>]*)*''>", "").replaceAll("[^\\x20-\\x7e]", "");//

				// LT = LT.replaceAll("\\<\\!D", "").replaceAll("\\]\\]\\>", "");//

				String NameF = NameFile.substring(0, 3);
				switch (NameF) {
				case "LTA": {
					JAXBContext jaxbContext = JAXBContext.newInstance(LTAGiornaliera.class);
					Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
					Utility.validateXmlLTA(unmarshaller);
					StringReader reader = new StringReader(LT);
					LTAGiornaliera LogT;
					try {
						
					 LogT = (LTAGiornaliera) unmarshaller.unmarshal(reader);
					 e.set(LogT);
					}catch (Exception e1) {
						log.error(e1);
					}
					
					// log.info("OK");
					break;
				}
				case "RCA": {
					JAXBContext jaxbContext = JAXBContext.newInstance(RiepilogoControlloAccessi.class);
					Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
					Utility.validateXmlRCA(unmarshaller);
					StringReader reader = new StringReader(LT);
					RiepilogoControlloAccessi LogT = (RiepilogoControlloAccessi) unmarshaller.unmarshal(reader);
					e.set(LogT);
					// log.info("OK");
					break;
				}
				case "RPG": {
					JAXBContext jaxbContext = JAXBContext.newInstance(RiepilogoGiornaliero.class);
					Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
					Utility.validateXmlRiepilogoGiornaliero(unmarshaller);
					StringReader reader = new StringReader(LT);
					RiepilogoGiornaliero RPG = (RiepilogoGiornaliero) unmarshaller.unmarshal(reader);
					e.set(RPG);
					// log.info("OK");
					break;
				}
				case "RPM": {
					JAXBContext jaxbContext = JAXBContext.newInstance(RiepilogoMensile.class);
					Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
					Utility.validateXmlRiepilogoMensile(unmarshaller);
					StringReader reader = new StringReader(LT);
					RiepilogoMensile RPM = (RiepilogoMensile) unmarshaller.unmarshal(reader);
					e.set(RPM);
					// log.info("OK");

					break;
				}
				case "LOG": {
					NameF = NameFile.substring(0, 5);
					if(NameF.equals("LOG_I")) {
						JAXBContext jaxbContext = JAXBContext.newInstance(LogSigillo.class);
						Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
						Utility.validateXmlLogSigillo(unmarshaller);

						StringReader reader = new StringReader(LT);
						LogSigillo logS = (LogSigillo)  unmarshaller.unmarshal(reader);
					}else {
					JAXBContext jaxbContext = JAXBContext.newInstance(LogTransazione.class);
					Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
					Utility.validateXmlLogTransazione(unmarshaller);

					StringReader reader = new StringReader(LT);
					LogTransazione LogT = (LogTransazione) unmarshaller.unmarshal(reader);
					e.set(LogT);
					}
					// log.info("OK");

					break;
				}

				default:
					break;
				}

				i++;
			}
			e.esame();
			/*
			 * { byte[] t = Utility.getData(your_primitive_bytes); String LogTransazione =
			 * new String(t); String LT =
			 * LogTransazione.replaceAll("<!DOCTYPE LTA_Giornaliera SYSTEM.*",
			 * "").replaceAll("[^\\x20-\\x7e]", ""); JAXBContext jaxbContext =
			 * JAXBContext.newInstance(LTAGiornaliera.class); Unmarshaller unmarshaller =
			 * jaxbContext.createUnmarshaller();
			 * Utility.validateXmlLogTransazione(unmarshaller);
			 * 
			 * StringReader reader = new StringReader(LT); LTAGiornaliera LogT =
			 * (LTAGiornaliera) unmarshaller.unmarshal(reader);
			 * 
			 * 
			 * }
			 */
			// log.info("Logs: [NProgressivi, Corrispettivo Lordo, Prevendita Lordo] "+sum);
			String text = "KO";
			return text;// new Log(sum);
			// throw new WebApplicationException(Response.status(406).entity(text).build());

		} catch (Exception e) {
			e.printStackTrace();
			log.error(e);
		}
		return null;
		// return "";

	}

	@Path("/SingleFileLTA")
	@POST
	@ApiResponse(responseCode = "200", content = @Content(mediaType = MediaType.APPLICATION_XML, schema = @Schema(implementation = String.class)), description = ".")
	@RequestBody(content = @Content(mediaType = MediaType.MULTIPART_FORM_DATA// ,
	// schema = @Schema(implementation = List<byte[]>.class)
	), description = ".")
	@Consumes(MediaType.MULTIPART_FORM_DATA)
	public String putLogTransazionel(@FormDataParam("file") InputStream uploadedInputStream,
			@FormDataParam("file") FormDataContentDisposition fileDetail, @Context HttpServletRequest request,
			@Context HttpServletResponse response) throws JAXBException {// DatiCorrispettiviType Corrispettivi,
		// @Context HttpServletRequest request){
		response.setHeader("Connection", "Close");
		log.info("****************FileRiepilogoControlloAccessi********************");
		try {

			log.info("Message from: " + request.getRemoteAddr());

			String text = "KO";
			return text;
			// throw new WebApplicationException(Response.status(406).entity(text).build());

		} catch (Exception e) {
			e.printStackTrace();
			log.error(e);
		}
		return "";

	}

}
